
############
#
# Copyright (c) 2023 Joseph DelPreto / MIT CSAIL and Project CETI
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR
# IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# Created 2023 by Joseph DelPreto [https://josephdelpreto.com].
#
############

############
# A class to speed up plotting for videos by drawing directly on image matrices.
############

import cv2
import numpy as np
import time
import pyqtgraph

from helpers_various import *

class ImagePlot:
  
  #########################################
  # Initialization
  #########################################
  def __init__(self, auto_update_empty_plot=True):
    
    # Overall configuration.
    self._plot_size = [480, 640]
    self._auto_update_empty_plot = auto_update_empty_plot
    self._padding_left = 0
    self._padding_top = 0
    self._padding_right = 0
    self._padding_bottom = 0
    self._axis_left_position_widthRatio = None
    self._axis_right_position_widthRatio = None
    self._img_empty = None
    self._img = None
    
    # Axis limits.
    self._xlim = [0, 10]
    self._ylim = [0, 10]
    self._equal_aspect_ratio = False
    
    # Axis labels.
    self._xlabel = 'X'
    self._ylabel = 'Y'
    
    # Axis ticks.
    self._show_tick_labels_x = True
    self._show_tick_labels_y = True
    self._x_tick_label_format = '%g'
    self._y_tick_label_format = '%g'
    # Specifying ticks by a desired spacing.
    self._x_tick_spacing = {'major': 1, 'minor': 1}
    self._y_tick_spacing = {'major': 1, 'minor': 1}
    self._x_tick_value_to_include = 0
    self._y_tick_value_to_include = 0
    # Specifying ticks by manual lists of values.
    self._xticks = {'major': [], 'minor': []}
    self._yticks = {'major': [], 'minor': []}
    
    # Grid lines.
    self._show_grid_x = {'major':True, 'minor':False}
    self._show_grid_y = {'major':True, 'minor':False}
    self._grid_color_bgr = {'major':(125, 125, 125), 'minor':(50, 50, 50)}
    self._grid_thickness = {'major':2, 'minor':2}
    
    # Box around the axes.
    self._show_box = True
    self._show_halfBox_bottomAndLeft = True
    self._box_thickness = 2
    self._box_color_bgr = (200, 200, 200)
    
    # Text formatting for labels and ticks.
    self._text_bg_color_bgr = (0, 0, 0)
    self._text_color_bgr = (150, 0, 0)
    self._font_scale = 1
    self._font_scale_ylabelHeightRatio = None
    self._font_thickness = 1
    self._font_face = cv2.FONT_HERSHEY_DUPLEX
    
    # Color bar state.
    self._colorbar_img = None
    self._colorbar_pad_to_axis = None
    
    # Initialize the empty plot.
    self._img_scratch = np.zeros(shape=(*self._plot_size, 3), dtype=np.uint8)
    self._img_scratch_rotated = np.zeros(shape=(self._plot_size[1], self._plot_size[0], 3), dtype=np.uint8)
    self.render_empty()
    self.clear_plot()
  
  ###########################################
  # Overall plot image layout
  ###########################################
  
  # Set the dimensions of the plot image that will be generated.
  def set_plot_size(self, width, height):
    self._plot_size = [height, width]
    # Initialize scratch images to use for testing font sizes.
    self._img_scratch = np.zeros(shape=(*self._plot_size, 3), dtype=np.uint8)
    self._img_scratch_rotated = np.zeros(shape=(self._plot_size[1], self._plot_size[0], 3), dtype=np.uint8)
    # Update the empty plot.
    if self._auto_update_empty_plot:
      self.render_empty()
  
  # Set padding from the edges of the plot image to where everything is drawn (including axis labels, ticks, etc)
  def set_padding(self, left, top, right, bottom):
    self._padding_left = int(left)
    self._padding_top = int(top)
    self._padding_right = int(right)
    self._padding_bottom = int(bottom)
    if self._auto_update_empty_plot:
      self.render_empty()
      
  # Manually specify where the x axis should start and end on the plot image.
  # @param width_ratio is the desired position as a fraction of entire plot image width
  #   after subtracting the specified plot padding (see set_plot_size() and set_padding()).
  # An example usage would be wanting to show two plots on top of each other
  #  and ensure that the x axes are aligned regardless of text sizes, colorbars, etc.
  # Note that checks will not currently be performed to ensure that the labels and ticks
  #  can fit if the axis position is manually specified, so errors may be thrown
  #  later if the axis is specified as too large.
  def set_axis_left_position(self, width_ratio):
    self._axis_left_position_widthRatio = width_ratio
    if self._auto_update_empty_plot:
      self.render_empty()
  def set_axis_right_position(self, width_ratio):
    self._axis_right_position_widthRatio = width_ratio
    if self._auto_update_empty_plot:
      self.render_empty()
  
  #########################################
  # Font for all text
  #########################################
  
  # Specify the font size for all text.
  # This includes axis labels and tick labels.
  # If size is specified, will use that size directly.
  # If yLabelHeightRatio is specified, will compute a font such that the
  #  vertical y axis label takes up that ratio of the entire plot image height.
  def set_font_size(self, size=None, yLabelHeightRatio=None, thickness=1):
    if size is not None:
      self._font_scale = size
      self._font_scale_ylabelHeightRatio = None
    elif yLabelHeightRatio is not None:
      self._font_scale_ylabelHeightRatio = yLabelHeightRatio
      self._font_scale = None
    self._font_thickness = thickness
    if self._auto_update_empty_plot:
      self.render_empty()
  
  # Specify the font color for all text.
  # @param color is in RGB format, with each entry scaled out of 255.
  # This includes axis labels and tick labels.
  # Color is specified in RGB format, with each entry scaled out of 255.
  def set_font_color(self, color):
    self._text_color_bgr = np.flip(color).tolist()
    if self._auto_update_empty_plot:
      self.render_empty()
  
  #########################################
  # x/y axis limits
  #########################################
  
  # Specify that the plot should have an equal aspect ratio, 
  # i.e. that x and y grid lines form squares if they have the same tick spacing.
  def set_equal_aspect_ratio(self, equal_aspect_ratio):
    self._equal_aspect_ratio = equal_aspect_ratio
    # Adjust the current limits to enforce an equal aspect ratio.
    # These calls will also render the empty plot if needed.
    if self._equal_aspect_ratio:
      if self._axis_size[0] > self._axis_size[1]:
        self.set_x_limits(self._xlim)
      else:
        self.set_y_limits(self._ylim)
  
  # Set the x axis limits.
  # It will also adjust the y axis limits if the plot is set to an equal aspect ratio.
  #  Will keep the y center coordinate unchanged.
  def set_x_limits(self, limits):
    old_limits = self._xlim
    self._xlim = limits
    # Adjust the y limits accordingly to maintain an equal aspect ratio if desired.
    if self._equal_aspect_ratio:
      self.render_empty()
      y_ratio = self._axis_size[0]/self._axis_size[1]
      yrange = (self._xlim[1] - self._xlim[0])*y_ratio
      ycenter = np.mean(self._ylim)
      self._ylim = ycenter + np.array([-1, 1])*yrange/2
    if self._auto_update_empty_plot and np.any(old_limits != self._xlim):
      self.render_empty()
  # Set the y axis limits.
  # It will also adjust the x axis limits if the plot is set to an equal aspect ratio.
  #  Will keep the x center coordinate unchanged.
  def set_y_limits(self, limits):
    old_limits = self._ylim
    self._ylim = limits
    # Adjust the x limits accordingly to maintain an equal aspect ratio if desired.
    if self._equal_aspect_ratio:
      self.render_empty()
      x_ratio = self._axis_size[1]/self._axis_size[0]
      xrange = (self._ylim[1] - self._ylim[0])*x_ratio
      xcenter = np.mean(self._xlim)
      self._xlim = xcenter + np.array([-1, 1])*xrange/2
    if self._auto_update_empty_plot and np.any(old_limits != self._ylim):
      self.render_empty()
  
  # Get the current x limits or x range.
  def get_x_limits(self):
    return self._xlim
  def get_x_range(self):
    return self._xlim[1] - self._xlim[0]
  # Get the current y limits or y range.
  def get_y_limits(self):
    return self._ylim
  def get_y_range(self):
    return self._ylim[1] - self._ylim[0]
  
  #########################################
  # Axis labels
  #########################################
  
  # Set the x axis label text.
  def set_x_label(self, label):
    self._xlabel = label
    if self._auto_update_empty_plot:
      self.render_empty()
  
  # Set the y axis label text.
  def set_y_label(self, label):
    self._ylabel = label
    if self._auto_update_empty_plot:
      self.render_empty()
  
  #########################################
  # Ticks
  # Major/minor grid lines will be drawn at major/minor ticks.
  #########################################
  
  # Specify whether tick labels should be shown for each axis.
  def show_tick_labels(self, x=True, y=True):
    self._show_tick_labels_x = x
    self._show_tick_labels_y = y
    if self._auto_update_empty_plot:
      self.render_empty()
  
  # Specify the string format that should be applied to tick values.
  def set_x_tick_label_format(self, format_str):
    self._x_tick_label_format = format_str
  def set_y_tick_label_format(self, format_str):
    self._y_tick_label_format = format_str
  
  # Define x ticks by specifying a desired spacing.
  # Optionally specify a value that should definitely be included as a tick, 
  #   instead of being potentially skipped by the spacing intervals.
  def set_x_ticks_spacing(self, major_interval, minor_interval, value_to_include=0):
    self.set_x_ticks_spacing_major(major_interval, value_to_include=value_to_include)
    self.set_x_ticks_spacing_minor(minor_interval, value_to_include=value_to_include)
  def set_x_ticks_spacing_major(self, spacing, value_to_include=0):
    self._x_tick_spacing['major'] = spacing
    self._x_tick_value_to_include = value_to_include
    if self._auto_update_empty_plot:
      self.render_empty()
  def set_x_ticks_spacing_minor(self, spacing, value_to_include=0):
    self._x_tick_spacing['minor'] = spacing
    self._x_tick_value_to_include = value_to_include
    if self._auto_update_empty_plot:
      self.render_empty()
  # Define y ticks by specifying a desired spacing.
  # Optionally specify a value that should definitely be included as a tick, 
  #   instead of being potentially skipped by the spacing intervals.
  def set_y_ticks_spacing(self, major_interval, minor_interval, value_to_include=0):
    self.set_y_ticks_spacing_major(major_interval, value_to_include=value_to_include)
    self.set_y_ticks_spacing_minor(minor_interval, value_to_include=value_to_include)
  def set_y_ticks_spacing_major(self, spacing, value_to_include=0):
    self._y_tick_spacing['major'] = spacing
    self._y_tick_value_to_include = value_to_include
    if self._auto_update_empty_plot:
      self.render_empty()
  def set_y_ticks_spacing_minor(self, spacing, value_to_include=0):
    self._y_tick_spacing['minor'] = spacing
    self._y_tick_value_to_include = value_to_include
    if self._auto_update_empty_plot:
      self.render_empty()
  
  # Define x ticks by explicitly specifying tick values.
  def set_x_ticks(self, major_tick_values, minor_tick_values):
    self.set_x_ticks_major(major_tick_values)
    self.set_x_ticks_minor(minor_tick_values)
  def set_x_ticks_major(self, tick_values):
    self._xticks['major'] = sorted(tick_values)
    if tick_values is not None:
      self._x_tick_spacing['major'] = None # use manual ticks instead of auto
    if self._auto_update_empty_plot:
      self.render_empty()
  def set_x_ticks_minor(self, tick_values):
    self._xticks['minor'] = sorted(tick_values)
    if tick_values is not None:
      self._x_tick_spacing['minor'] = None # use manual ticks instead of auto
    if self._auto_update_empty_plot:
      self.render_empty()
  # Define y ticks by explicitly specifying tick values.
  def set_y_ticks(self, major_tick_values, minor_tick_values):
    self.set_y_ticks_major(major_tick_values)
    self.set_y_ticks_minor(minor_tick_values)
  def set_y_ticks_major(self, tick_values):
    self._yticks['major'] = sorted(tick_values)
    if tick_values is not None:
      self._y_tick_spacing['major'] = None # use manual ticks instead of auto
    if self._auto_update_empty_plot:
      self.render_empty()
  def set_y_ticks_minor(self, tick_values):
    self._yticks['minor'] = sorted(tick_values)
    if tick_values is not None:
      self._y_tick_spacing['minor'] = None # use manual ticks instead of auto
    if self._auto_update_empty_plot:
      self.render_empty()
  
  # Compute tick values if spacing was specified rather than explicit values.
  def _update_tick_values(self):
    for tick_type in ['minor', 'major']:
      if self._x_tick_spacing[tick_type] is not None:
        first_tick = next_multiple(self._xlim[0], self._x_tick_spacing[tick_type])
        last_tick = previous_multiple(self._xlim[1], self._x_tick_spacing[tick_type])
        (first_tick, last_tick) = sorted([first_tick, last_tick])
        self._xticks[tick_type] = np.arange(start=first_tick, stop=last_tick+self._x_tick_spacing[tick_type]/2, # add to the stop to be inclusive of last_tick
                                            step=self._x_tick_spacing[tick_type])
        # Ensure that the specified value to include is a tick.
        offset_toAdd = self._x_tick_value_to_include - previous_multiple(self._x_tick_value_to_include, self._x_tick_spacing[tick_type])
        self._xticks[tick_type] += offset_toAdd
      if self._y_tick_spacing[tick_type] is not None:
        first_tick = next_multiple(self._ylim[0], self._y_tick_spacing[tick_type])
        last_tick = previous_multiple(self._ylim[1], self._y_tick_spacing[tick_type])
        (first_tick, last_tick) = sorted([first_tick, last_tick])
        self._yticks[tick_type] = np.arange(start=first_tick, stop=last_tick+self._y_tick_spacing[tick_type]/2, # add to the stop to be inclusive of last_tick
                                            step=self._y_tick_spacing[tick_type])
        # Ensure that the specified value to include is a tick.
        offset_toAdd = self._y_tick_value_to_include - previous_multiple(self._y_tick_value_to_include, self._y_tick_spacing[tick_type])
        self._yticks[tick_type] += offset_toAdd
  
  #########################################
  # Grid lines and axis box
  # Major/minor grid lines will be drawn at major/minor ticks.
  #########################################
  
  # Specify whether grid lines should be drawn for each axis.
  # Also configure the gird line color and thickness.
  # Color is specified in RGB format, with each entry scaled out of 255.
  def show_grid_major(self, x=True, y=True, color=None, thickness=None):
    self._show_grid_x['major'] = x
    self._show_grid_y['major'] = y
    if color is not None:
      self._grid_color_bgr['major'] = np.flip(color).tolist()
    if thickness is not None:
      self._grid_thickness['major'] = thickness
    if self._auto_update_empty_plot:
      self.render_empty()
  def show_grid_minor(self, x=True, y=True, color=None, thickness=None):
    self._show_grid_x['minor'] = x
    self._show_grid_y['minor'] = y
    if color is not None:
      self._grid_color_bgr['minor'] = np.flip(color).tolist()
    if thickness is not None:
      self._grid_thickness['minor'] = thickness
    if self._auto_update_empty_plot:
      self.render_empty()
      
  # Specify whether a box should be drawn around the axis area.
  # Color is specified in RGB format, with each entry scaled out of 255.
  def show_box(self, show, color=None, thickness=None):
    self._show_box = show
    if color is not None:
      self._box_color_bgr = np.flip(color).tolist()
    if thickness is not None:
      self._box_thickness = thickness
    if self._auto_update_empty_plot:
      self.render_empty()
  
  # Specify whether the bottom and left outlines of the axis area should be drawn (half box).
  # Color is specified in RGB format, with each entry scaled out of 255.
  def show_halfbox_bottomAndLeft(self, show, color=None, thickness=None):
    self._show_halfBox_bottomAndLeft = show
    if color is not None:
      self._box_color_bgr = np.flip(color).tolist()
    if thickness is not None:
      self._box_thickness = thickness
    if self._auto_update_empty_plot:
      self.render_empty()
  
  #########################################
  # Color bar
  #########################################
  
  # Determine the height of the area for a colorbar.
  # This can be useful for computing a color lookup table when adding a colorbar.
  def get_colorbar_area_height(self):
    self.render_empty()
    bottom = int(self._axis_bottomleft_position[0])
    top = int(self._axis_bottomleft_position[0] - self._axis_size[0])
    return int((bottom - top) + 1)
  
  # Add a color bar to the plot image.
  # Will be oriented vertically and on the right of the axes.
  # The width is the width of the color bar itself, excluding tick/colorbar labels and padding.
  #   If width is < 1, will interpret it as a fraction of the plot image width.
  #   Otherwise, will be interpreted as pixels.
  # label_padding will be added between the color bar and tick labels, and between tick labels and the main label.
  # pad_to_axis will be added between the right side of the axis and the color bar.
  # color_lookup_or_colormap can either be:
  #  A PyQtGraph ColorMap object with stops ranging from 0 to 1.
  #    For example: pyqtgraph.colormap.get('gist_stern', source='matplotlib', skipCache=True)
  #  A matrix that specifies the color to use for each pixel row in the drawn color bar.
  #    It should be an Nx3 matrix where N is get_colorbar_area_height()
  #    and each row is a color for that pixel row in RGB format scaled out of 255.
  def add_colorbar(self, color_lookup_or_colormap_rgb, width, limits, ticks=None, 
                   label='', 
                   pad_to_axis=10, label_padding=5, 
                   tick_label_format='%g'):
    if ticks is None:
      ticks = []
    
    # Determine the vertical size of the area for the colorbar.
    self.render_empty()
    bottom = int(self._axis_bottomleft_position[0])
    top = int(self._axis_bottomleft_position[0] - self._axis_size[0])
    height = int((bottom - top) + 1)
    
    # Determine size of tick labels and of main label.
    tick_labels = [tick_label_format % tick for tick in ticks]
    tick_dims = [draw_text_on_image(self._img_scratch, tick_label, pos=(0.5, 0.5), 
                                    text_width_ratio=None, font_scale=self._font_scale, 
                                    font_thickness=self._font_thickness, font=self._font_face, 
                                    text_color_bgr=self._text_color_bgr, text_bg_color_bgr=self._text_bg_color_bgr, 
                                    text_bg_outline_color_bgr=None, text_bg_pad_width_ratio=0, 
                                    preview_only=True, 
                                    ) for tick_label in tick_labels]
    tick_widths = [int(w) for (w, h, f, p) in tick_dims]
    tick_heights = [int(h) for (w, h, f, p) in tick_dims]
    if len(label) > 0:
      label_font_scale = self._font_scale
      label_dims = draw_text_on_image(self._img_scratch_rotated, label, pos=(0.5, 0.5), 
                                      text_width_ratio=None, font_scale=label_font_scale, 
                                      font_thickness=self._font_thickness, font=self._font_face, 
                                      text_color_bgr=self._text_color_bgr, text_bg_color_bgr=self._text_bg_color_bgr, text_bg_outline_color_bgr=None, text_bg_pad_width_ratio=0, 
                                      preview_only=True, 
                                      )
      # If the label is too big for the plot height, scale it to fit.
      if label_dims[0] > height: # compare width to height since the label will be rotated 90 degrees
        label_dims = draw_text_on_image(self._img_scratch_rotated, label, pos=(0.5, 0.5), 
                                        text_width_ratio=0.95, font_scale=None, 
                                        font_thickness=self._font_thickness, font=self._font_face, 
                                        text_color_bgr=self._text_color_bgr, text_bg_color_bgr=self._text_bg_color_bgr, text_bg_outline_color_bgr=None, text_bg_pad_width_ratio=0, 
                                        preview_only=True, 
                                        )
      (label_width, label_height, label_font_scale, _) = label_dims
    else:
      (label_width, label_height) = (0, 0)
    label_height = int(label_height*1.0) # scale to account for undershoot under the text baseline
    
    # Create an image for the colorbar of the appropriate size.
    if width < 1:
      width = round(width * self._plot_size[1])
    img_width =  width
    if len(ticks) > 0:
      img_width += label_padding + max(tick_widths)
    if len(label) > 0:
      img_width += label_padding + label_height
    img = np.zeros(shape=(height, img_width, 3), dtype=np.uint8)
    
    # Create a helper that maps from y coordinate of the colorbar to pixels.
    def colorbar_y_to_pixels(y):
      y_fraction = (y - limits[0]) / (limits[1] - limits[0])
      y_pixel = round(bottom - height * y_fraction)
      return y_pixel
    
    # Add tick labels.
    for (tick_index, tick) in enumerate(ticks):
      tick_label = tick_labels[tick_index]
      x = width + label_padding
      y = colorbar_y_to_pixels(tick) - tick_heights[tick_index]
      if y < 0:
        y = 0
      if y + tick_heights[tick_index] > height:
        y = height - tick_heights[tick_index]
      draw_text_on_image(img, tick_label, pos=(x, y), 
                         text_width_ratio=None, font_scale=self._font_scale, 
                         font_thickness=self._font_thickness, font=self._font_face, 
                         text_color_bgr=self._text_color_bgr, text_bg_color_bgr=self._text_bg_color_bgr, text_bg_outline_color_bgr=None, text_bg_pad_width_ratio=0, 
                         preview_only=False, 
                         )
    # Add the main label.
    if len(label) > 0:
      label_img = np.zeros(shape=(label_height, height, 3), dtype=np.uint8)
      draw_text_on_image(label_img, label, pos=(0.5, 0.5), 
                         text_width_ratio=None, font_scale=label_font_scale, 
                         font_thickness=self._font_thickness, font=self._font_face, 
                         text_color_bgr=self._text_color_bgr, text_bg_color_bgr=self._text_bg_color_bgr, text_bg_outline_color_bgr=None, text_bg_pad_width_ratio=0, 
                         preview_only=False, 
                         )
      label_img = np.flipud(np.transpose(label_img, axes=[1, 0, 2]))
      img[:, (img_width-label_height):(img_width+1), :] = label_img
    
    # Add colors.
    # Compute a color lookup if a PyQtGraph colormap was provided.
    if isinstance(color_lookup_or_colormap_rgb, pyqtgraph.colormap.ColorMap):
      color_lookup_or_colormap_rgb = color_lookup_or_colormap_rgb.getLookupTable(start=0, stop=1, nPts=height)
    for y in range(height):
      img[(height-1)-y, 0:width, :] = np.flip(color_lookup_or_colormap_rgb[y])
    
    # Store result and configuration.
    self._colorbar_img = img
    self._colorbar_pad_to_axis = int(pad_to_axis)
    
    # If the plot is set to having an equal aspect ratio, 
    #  update the limits now since adding the colorbar shrunk the
    #  axis horizonally and thus changed the axis aspect ratio.
    self.set_equal_aspect_ratio(self._equal_aspect_ratio)
    
    # Update the plot.
    self.render_empty()
  
  
  
  
  
  
  #########################################
  # Helpers for rendering the empty plot
  #########################################
  
  # Get an image with the y label drawn, and measure its size.
  def _get_ylabel_img(self, scratch_img=None, width_ratio=0.9):
    if scratch_img is None:
      scratch_img = self._img_scratch_rotated
    changed_font_size = False
    
    # Determine the size of the y label.
    # If desired, determine a font scale that will make the y label fit nicely.
    if len(self._ylabel) > 0:
      ylabel_width, ylabel_height, font_scale, _ = draw_text_on_image(scratch_img, self._ylabel, pos=(0, 0), 
                                                                      text_width_ratio=self._font_scale_ylabelHeightRatio, font_scale=self._font_scale, 
                                                                      font_thickness=self._font_thickness, font=self._font_face, 
                                                                      text_color_bgr=self._text_color_bgr, text_bg_color_bgr=self._text_bg_color_bgr, text_bg_outline_color_bgr=None, text_bg_pad_width_ratio=0, 
                                                                      preview_only=True, 
                                                                      )
      # If the label is too big to fit, scale the font size (for this label and for all other text).
      if ylabel_width > self._plot_size[0]*width_ratio:
        ylabel_width, ylabel_height, font_scale, _ = draw_text_on_image(scratch_img, self._ylabel, pos=(0, 0), 
                                                                        text_width_ratio=width_ratio, font_scale=None, 
                                                                        font_thickness=self._font_thickness, font=self._font_face, 
                                                                        text_color_bgr=self._text_color_bgr, text_bg_color_bgr=self._text_bg_color_bgr, text_bg_outline_color_bgr=None, text_bg_pad_width_ratio=0, 
                                                                        preview_only=True, 
                                                                        )
        changed_font_size = (font_scale != self._font_scale)
        self._font_scale = font_scale

      # Scale the height to account for undershoot under the text baseline.
      ylabel_height = round(ylabel_height*2.0)

      # Create an image with the y label text.
      ylabel_img = np.zeros(shape=(ylabel_height, ylabel_width, 3), dtype=np.uint8)
      draw_text_on_image(ylabel_img, self._ylabel, pos=(0.5, 0.5), 
                         text_width_ratio=None, font_scale=self._font_scale, 
                         font_thickness=self._font_thickness, font=self._font_face, 
                         text_color_bgr=self._text_color_bgr, text_bg_color_bgr=self._text_bg_color_bgr, text_bg_outline_color_bgr=None, text_bg_pad_width_ratio=0, 
                         preview_only=False, 
                         )
      ylabel_img = np.flipud(np.transpose(ylabel_img, axes=[1, 0, 2]))
    else:
      ylabel_width = 0
      ylabel_height = 0
      ylabel_img = None
    
    return (ylabel_img, ylabel_height, ylabel_width, changed_font_size)
  
  # Get an image with the x label drawn, and measure its size.
  def _get_xlabel_img(self, scratch_img=None, width_ratio=0.9):
    if scratch_img is None:
      scratch_img = self._img_scratch
    changed_font_size = False
    
    # Determine the size of the x label.
    if len(self._xlabel) > 0:
      xlabel_width, xlabel_height, _, _ = draw_text_on_image(scratch_img, self._xlabel, pos=(0, 0), 
                                                             text_width_ratio=None, font_scale=self._font_scale, 
                                                             font_thickness=self._font_thickness, font=self._font_face, 
                                                             text_color_bgr=self._text_color_bgr, text_bg_color_bgr=self._text_bg_color_bgr, text_bg_outline_color_bgr=None, text_bg_pad_width_ratio=0, 
                                                             preview_only=True, 
                                                             )
      # If the label is too big to fit, scale the font size (for this label and for all other text).
      if xlabel_width > self._plot_size[1]*width_ratio:
        xlabel_width, xlabel_height, font_scale, _ = draw_text_on_image(scratch_img, self._xlabel, pos=(0, 0), 
                                                                        text_width_ratio=width_ratio, font_scale=None, 
                                                                        font_thickness=self._font_thickness, font=self._font_face, 
                                                                        text_color_bgr=self._text_color_bgr, text_bg_color_bgr=self._text_bg_color_bgr, text_bg_outline_color_bgr=None, text_bg_pad_width_ratio=0, 
                                                                        preview_only=True, 
                                                                        )
        changed_font_size = (font_scale != self._font_scale)
        self._font_scale = font_scale
      
      # Scale the height to account for undershoot under the text baseline.
      xlabel_height = round(xlabel_height*2)
      
      # Create an image with the x label text.
      xlabel_img = np.zeros(shape=(xlabel_height, xlabel_width, 3), dtype=np.uint8)
      draw_text_on_image(xlabel_img, self._xlabel, pos=(0.5, 0.5), 
                         text_width_ratio=None, font_scale=self._font_scale, 
                         font_thickness=self._font_thickness, font=self._font_face, 
                         text_color_bgr=self._text_color_bgr, text_bg_color_bgr=self._text_bg_color_bgr, text_bg_outline_color_bgr=None, text_bg_pad_width_ratio=0, 
                         preview_only=False, 
                         )
    else:
      xlabel_height = 0
      xlabel_width = 0
      xlabel_img = None
      
    return (xlabel_img, xlabel_height, xlabel_width, changed_font_size)
  
  # Get the size of x tick labels.
  def _get_xtick_labels(self):
    xtick_labels = [self._x_tick_label_format % tick for tick in self._xticks['major']]
    xtick_dims = [draw_text_on_image(self._img_scratch, xtick_label, pos=(0, 0), 
                                     text_width_ratio=None, font_scale=self._font_scale, 
                                     font_thickness=self._font_thickness, font=self._font_face, 
                                     text_color_bgr=self._text_color_bgr, text_bg_color_bgr=self._text_bg_color_bgr, text_bg_outline_color_bgr=None, text_bg_pad_width_ratio=0, 
                                     preview_only=True, 
                                     ) for xtick_label in xtick_labels]
    xtick_widths = [w for (w, h, f, p) in xtick_dims]
    xtick_heights = [round(h*1.0) for (w, h, f, p) in xtick_dims] # scale to account for undershoot under the text baseline
    if not self._show_tick_labels_x:
      xtick_widths = [0]*len(xtick_widths)
      xtick_heights = [0]*len(xtick_heights)
      xtick_labels = ['']*len(xtick_labels)
    return (xtick_labels, xtick_heights, xtick_widths)
    
  # Get the size of y tick labels.
  def _get_ytick_labels(self):
    ytick_labels = [self._y_tick_label_format % tick for tick in self._yticks['major']]
    ytick_dims = [draw_text_on_image(self._img_scratch, ytick_label, pos=(0, 0), 
                                     text_width_ratio=None, font_scale=self._font_scale, 
                                     font_thickness=self._font_thickness, font=self._font_face, 
                                     text_color_bgr=self._text_color_bgr, text_bg_color_bgr=self._text_bg_color_bgr, text_bg_outline_color_bgr=None, text_bg_pad_width_ratio=0, 
                                     preview_only=True, 
                                     ) for ytick_label in ytick_labels]
    ytick_widths = [w for (w, h, f, p) in ytick_dims]
    ytick_heights = [round(h*1.0) for (w, h, f, p) in ytick_dims] # scale to account for undershoot under the text baseline
    if not self._show_tick_labels_y:
      ytick_widths = [0]*len(ytick_widths)
      ytick_heights = [0]*len(ytick_heights)
      ytick_labels = ['']*len(ytick_labels)
    return (ytick_labels, ytick_heights, ytick_widths)
  
  #########################################
  # Render the empty plot, effectively applying all specified configurations.
  #########################################
  
  def render_empty(self):
    # Update the padding to account for the box thickness.
    top_pad = self._padding_top + (np.ceil(self._box_thickness/2) if self._show_box else 0)
    right_pad = self._padding_right + (np.ceil(self._box_thickness/2) if self._show_box else 0)
    left_pad =  self._padding_left
    bottom_pad =  self._padding_bottom
    
    # Initialize the empty image.
    self._img_empty = np.zeros(shape=(*self._plot_size, 3), dtype=np.uint8)
    
    # Create an image with the y label text.
    (ylabel_img, ylabel_height, ylabel_width, changed_font_size) = self._get_ylabel_img()
    
    # Create an image with the x label text.
    (xlabel_img, xlabel_height, xlabel_width, changed_font_size) = self._get_xlabel_img()
    # Recreate the y label image if the font size changed.
    if changed_font_size:
      (ylabel_img, ylabel_height, ylabel_width, changed_font_size) = self._get_ylabel_img()
    
    # Determine tick locations based on manual locations or on spacing.
    self._update_tick_values()
    
    # Get tick labels and their sizes.
    (xtick_labels, xtick_heights, xtick_widths) = self._get_xtick_labels()
    (ytick_labels, ytick_heights, ytick_widths) = self._get_ytick_labels()
    xticks_height = max(xtick_heights)
    yticks_width = max(ytick_widths)
    
    # Determine size of labels and ticks, with padding.
    ylabel_height_padded = ylabel_height + max(2.0, ylabel_height*0.1)
    ylabel_width_padded = ylabel_width + max(2.0, ylabel_width*0.1)
    xlabel_height_padded = xlabel_height + max(2.0, xlabel_height*0.1)
    xlabel_width_padded = xlabel_width + max(2.0, xlabel_width*0.1)
    xticks_height_padded = xticks_height + max([2.0, xticks_height*0.5])
    yticks_width_padded = yticks_width + max([2.0, yticks_width*0.1])
    
    # Determine position and size of the axis area.
    axis_x_left_offset = round(yticks_width_padded + ylabel_height_padded + left_pad + self._box_thickness/2)
    axis_y_bottom_offset = round(xticks_height_padded + xlabel_height_padded + bottom_pad + self._box_thickness/2)
    axis_y_top_offset = top_pad
    axis_x_right_offset = right_pad
    if self._colorbar_img is not None:
      axis_x_right_offset += self._colorbar_img.shape[1] + self._colorbar_pad_to_axis
    self._axis_bottomleft_position = [self._plot_size[0] - axis_y_bottom_offset, axis_x_left_offset]
    self._axis_size = [self._plot_size[0] - axis_y_bottom_offset - axis_y_top_offset, 
                       self._plot_size[1] - axis_x_left_offset - axis_x_right_offset]
    # Override with manually specified left/right locations if desired.
    if self._axis_left_position_widthRatio is not None:
      axis_right_position = self._axis_bottomleft_position[1] + self._axis_size[1]
      self._axis_bottomleft_position[1] = round(left_pad + self._axis_left_position_widthRatio * (self._plot_size[1] - left_pad - right_pad))
      self._axis_size[1] = axis_right_position - self._axis_bottomleft_position[1]
    if self._axis_right_position_widthRatio is not None:
      axis_right_position = round(self._axis_right_position_widthRatio * (self._plot_size[1] - left_pad - right_pad) - right_pad)
      self._axis_size[1] = axis_right_position - self._axis_bottomleft_position[1]
    self._axis_size = [int(self._axis_size[0]), int(self._axis_size[1])]
    
    # Make font sizes smaller if needed, now that the axis size is known.
    if xlabel_width > self._axis_size[1]:
      scratch_img = np.zeros(shape=(self._axis_size[0], self._axis_size[1], 3), dtype=np.uint8)
      (xlabel_img, xlabel_height, xlabel_width, changed_font_size) = self._get_xlabel_img(scratch_img=scratch_img, width_ratio=0.99)
    if ylabel_width > self._axis_size[0]:
      scratch_img = np.zeros(shape=(self._axis_size[1], self._axis_size[0], 3), dtype=np.uint8)
      (ylabel_img, ylabel_height, ylabel_width, changed_font_size) = self._get_ylabel_img(scratch_img=scratch_img, width_ratio=0.99)
      
    # Add the y axis label to the empty image.
    # It will be centered to the axis area.
    if ylabel_img is not None:
      ylabel_center_x = self._axis_bottomleft_position[1] - yticks_width_padded - ylabel_height_padded//2
      ylabel_center_y = self._axis_bottomleft_position[0] - self._axis_size[0]/2
      ylabel_top_y = round(ylabel_center_y - ylabel_width/2)
      ylabel_bottom_y = ylabel_top_y + ylabel_width - 1
      ylabel_left_x = round(ylabel_center_x - ylabel_height/2)
      ylabel_right_x = ylabel_left_x + ylabel_height - 1
      self._img_empty[ylabel_top_y:(ylabel_bottom_y+1), ylabel_left_x:(ylabel_right_x+1), :] = ylabel_img
    
    # Add the x axis label to the empty image.
    # It will be centered to the axis area.
    if xlabel_img is not None:
      xlabel_center_x = self._axis_bottomleft_position[1] + self._axis_size[1]/2
      xlabel_center_y = self._plot_size[0] - xlabel_height_padded/2 - bottom_pad
      xlabel_top_y = round(xlabel_center_y - xlabel_height/2)
      xlabel_bottom_y = xlabel_top_y + xlabel_height - 1
      xlabel_left_x = round(xlabel_center_x - xlabel_width/2)
      xlabel_right_x = xlabel_left_x + xlabel_width - 1
      self._img_empty[xlabel_top_y:(xlabel_bottom_y+1), xlabel_left_x:(xlabel_right_x+1), :] = xlabel_img
    
    # Add x tick labels.
    if self._show_tick_labels_x:
      ticklabel_top_y = round(self._axis_bottomleft_position[0] + (xticks_height_padded-xticks_height)/2 + self._box_thickness/2)
      for (tick_index, x) in enumerate(self._xticks['major']):
        if x < self._xlim[0] or x > self._xlim[1]:
          continue
        label = xtick_labels[tick_index]
        label_width = xtick_widths[tick_index]
        ticklabel_center_x, _ = self._coordinates_to_pixels(x, 0)
        ticklabel_left_x = round(ticklabel_center_x - label_width/2)
        draw_text_on_image(self._img_empty, label, pos=(ticklabel_left_x, ticklabel_top_y), 
                           text_width_ratio=None, font_scale=self._font_scale, 
                           font_thickness=self._font_thickness, font=self._font_face, 
                           text_color_bgr=self._text_color_bgr, text_bg_color_bgr=self._text_bg_color_bgr, text_bg_outline_color_bgr=None, text_bg_pad_width_ratio=0, 
                           preview_only=False, 
                           )
    # Add y tick labels.
    if self._show_tick_labels_y:
      ticklabel_right_x = round(self._axis_bottomleft_position[1] - (yticks_width_padded-yticks_width)/2 - self._box_thickness/2)
      for (tick_index, y) in enumerate(self._yticks['major']):
        if y < self._ylim[0] or y > self._ylim[1]:
          continue
        label = ytick_labels[tick_index]
        label_width = ytick_widths[tick_index]
        label_height = ytick_heights[tick_index]
        ticklabel_left_x = ticklabel_right_x - label_width
        _, ticklabel_center_y = self._coordinates_to_pixels(0, y)
        ticklabel_top_y = round(ticklabel_center_y - label_height/2)
        if ticklabel_top_y < 0:
          ticklabel_top_y = 0
        if ticklabel_top_y + label_height > self._plot_size[0]:
          ticklabel_top_y = self._plot_size[0] - label_height
        draw_text_on_image(self._img_empty, label, pos=(ticklabel_left_x, ticklabel_top_y), 
                           text_width_ratio=None, font_scale=self._font_scale, 
                           font_thickness=self._font_thickness, font=self._font_face, 
                           text_color_bgr=self._text_color_bgr, text_bg_color_bgr=self._text_bg_color_bgr, text_bg_outline_color_bgr=None, text_bg_pad_width_ratio=0, 
                           preview_only=False, 
                           )
    
    # Add grid lines.
    for grid_type in ['minor', 'major']:
      if self._show_grid_x[grid_type]:
        for (tick_index, x) in enumerate(self._xticks[grid_type]):
          if x < self._xlim[0] or x > self._xlim[1]:
            continue
          bottom_pos = self._coordinates_to_pixels(x=x, y=self._ylim[0])
          top_pos = self._coordinates_to_pixels(x=x, y=self._ylim[1])
          cv2.line(self._img_empty, bottom_pos, top_pos, self._grid_color_bgr[grid_type], self._grid_thickness[grid_type])
      if self._show_grid_y[grid_type]:
        for (tick_index, y) in enumerate(self._yticks[grid_type]):
          if y < self._ylim[0] or y > self._ylim[1]:
            continue
          left_pos = self._coordinates_to_pixels(x=self._xlim[0], y=y)
          right_pos = self._coordinates_to_pixels(x=self._xlim[1], y=y)
          cv2.line(self._img_empty, left_pos, right_pos, self._grid_color_bgr[grid_type], self._grid_thickness[grid_type])
      
    # Get positions of the axis area.
    bottomleft_pos = self._coordinates_to_pixels(x=self._xlim[0], y=self._ylim[0])
    bottomright_pos = self._coordinates_to_pixels(x=self._xlim[1], y=self._ylim[0])
    topleft_pos = self._coordinates_to_pixels(x=self._xlim[0], y=self._ylim[1])
    topright_pos = self._coordinates_to_pixels(x=self._xlim[1], y=self._ylim[1])
    
    # Add bottom and left lines of the axis area if desired.
    if self._show_halfBox_bottomAndLeft:
      cv2.line(self._img_empty, bottomleft_pos, bottomright_pos, self._box_color_bgr, self._box_thickness)
      cv2.line(self._img_empty, bottomleft_pos, topleft_pos, self._box_color_bgr, self._box_thickness)
    
    # Add box if desired.
    if self._show_box:
      cv2.line(self._img_empty, topleft_pos, topright_pos, self._box_color_bgr, self._box_thickness)
      cv2.line(self._img_empty, bottomright_pos, topright_pos, self._box_color_bgr, self._box_thickness)
      
    # Add colorbar if desired.
    if self._colorbar_img is not None:
      left = int(self._axis_bottomleft_position[1] + self._axis_size[1] + self._colorbar_pad_to_axis)
      right = int(left + self._colorbar_img.shape[1] - 1)
      bottom = int(self._axis_bottomleft_position[0])
      top = int(bottom - (self._colorbar_img.shape[0] - 1))
      self._img_empty[top:(bottom+1), left:(right+1), :] = self._colorbar_img
  
  # Clear the plot by merely copying the pre-computing empty plot.
  def clear_plot(self):
    self._img = self._img_empty.copy()
  
  # Get the rendered empty plot image.
  # Will be in RGB format.
  def get_empty_plot_image(self):
    return cv2.cvtColor(self._img_empty, cv2.COLOR_BGR2RGB)
  
  # Show the empty plot.
  def show_empty_plot(self, window_title='Great emptiness!', block=False):
    self.render_empty()
    cv2.imshow(window_title, self._img_empty)
    cv2.waitKey(0 if block else 1)
  
  #########################################
  # Plot!
  #########################################
  
  # Convert from plot coordinates to image pixels.
  def _coordinates_to_pixels(self, x, y):
    x_fraction = (x - self._xlim[0]) / (self._xlim[1] - self._xlim[0])
    y_fraction = (y - self._ylim[0]) / (self._ylim[1] - self._ylim[0])
    x_pixel = round(self._axis_bottomleft_position[1] + self._axis_size[1] * x_fraction)
    y_pixel = round(self._axis_bottomleft_position[0] - self._axis_size[0] * y_fraction)
    return (x_pixel, y_pixel)
  
  # Plot a sequence of points.
  # Will connect the points by a line if line_thickness > 0.
  # Will draw a marker at each point if marker_symbols is not None.
  # Colors are specified in RGB format, with each entry scaled out of 255.
  # marker_symbols can be None, a symbol type, or a list of symbol types.
  #   Symbol types can be 'circle', 'square', 'triangle', or 'diamond'
  #   If a list is provided, it specifies a symbol to use for each point.
  def plot(self, x, y, 
           line_thickness=1, 
           color=(255, 255, 255), 
           marker_symbols='circle', 
           marker_size=2, marker_edge_thickness=0, marker_edge_color=(255, 255, 255)):
    # Check input arguments.
    if not isinstance(x, (list, tuple, np.ndarray)):
      x = [x]
    if not isinstance(y, (list, tuple, np.ndarray)):
      y = [y]
    color_bgr = np.flip(color).tolist()
    marker_edge_color_bgr = np.flip(marker_edge_color).tolist()
    
    # Draw the line segments connecting points.
    # If a line would intersect with the axis limits, will only draw to that intersection.
    # If a point in the middle of the sequence is outside the axis limits, 
    #  will draw disjoint line segments that each end at the appropriate axis intersections.
    if len(x) > 1 and line_thickness > 0:
      polylines = [[]]
      for point_index in range(1, len(x)):
        x_forSegment = [x[point_index-1], x[point_index]]
        y_forSegment = [y[point_index-1], y[point_index]]
        # Ignore the segment if it is entirely outside the axis area.
        if x_forSegment[0] < self._xlim[0] and x_forSegment[1] < self._xlim[0]:
          continue
        if x_forSegment[0] > self._xlim[1] and x_forSegment[1] > self._xlim[1]:
          continue
        if y_forSegment[0] < self._ylim[0] and y_forSegment[1] < self._ylim[0]:
          continue
        if y_forSegment[0] > self._ylim[1] and y_forSegment[1] > self._ylim[1]:
          continue
        # If one of the points is outside the axis area, draw a line to the axis intersection.
        # If the last point is outside, will start a new line segment next time
        #  since the plotted line should be disjoint in that case.
        end_current_line = False
        try:
          m = (y_forSegment[1] - y_forSegment[0])/(x_forSegment[1] - x_forSegment[0])
          b = (y_forSegment[1] - m*x_forSegment[1])
        except ZeroDivisionError:
          m = np.nan
          b = np.nan
        for i in range(2):
          if x_forSegment[i] < self._xlim[0]:
            x_forSegment[i] = self._xlim[0]
            y_forSegment[i] = (self._xlim[0]*m + b)
            end_current_line = (i == 1)
          if x_forSegment[i] > self._xlim[1]:
            x_forSegment[i] = self._xlim[1]
            y_forSegment[i] = (self._xlim[1]*m + b)
            end_current_line = (i == 1)
          if y_forSegment[i] < self._ylim[0]:
            y_forSegment[i] = self._ylim[0]
            if not np.isnan(m):
              x_forSegment[i] = (self._ylim[0] - b)/m
            end_current_line = (i == 1)
          if y_forSegment[i] > self._ylim[1]:
            y_forSegment[i] = self._ylim[1]
            if not np.isnan(m):
              x_forSegment[i] = (self._ylim[1] - b)/m
            end_current_line = (i == 1)
        # Add the point to the polyline segment.
        if len(polylines[-1]) == 0:
          polylines[-1].append(self._coordinates_to_pixels(x_forSegment[0], y_forSegment[0]))
        polylines[-1].append(self._coordinates_to_pixels(x_forSegment[1], y_forSegment[1]))
        if end_current_line:
          polylines.append([])
      # Draw the line segments.
      for polyline in polylines:
        cv2.polylines(self._img, [np.reshape(polyline, (-1, 1, 2))], False, color_bgr, line_thickness)
    
    # Draw the markers on top.
    if marker_symbols is not None:
      if not isinstance(marker_symbols, (list, tuple)):
        marker_symbols = [marker_symbols]*len(x)
      for i in range(len(x)):
        if x[i] < self._xlim[0] or x[i] > self._xlim[1]:
          continue
        if y[i] < self._ylim[0] or y[i] > self._ylim[1]:
          continue
        (x_i, y_i) = self._coordinates_to_pixels(x[i], y[i])
        if marker_symbols[i].lower() == 'circle':
          # Draw the filled marker.
          cv2.circle(self._img, (x_i, y_i), radius=int(np.ceil(marker_size/2)), 
                     color=color_bgr, thickness=-1) # -1 fills the shape
          # Draw the edge on top.
          if marker_edge_thickness is not None and marker_edge_thickness > 0:
            cv2.circle(self._img, (x_i, y_i), radius=int(np.ceil(marker_size/2)), 
                       color=marker_edge_color_bgr, thickness=marker_edge_thickness)
        if marker_symbols[i].lower() == 'square':
          topleft = [int(x_i - np.ceil(marker_size/2)), int(y_i - np.ceil(marker_size/2))]
          bottomright = [int(x_i + np.ceil(marker_size/2)), int(y_i + np.ceil(marker_size/2))]
          # Draw the filled marker.
          cv2.rectangle(self._img, topleft, bottomright, 
                        color_bgr, -1) # -1 fills the shape
          # Draw the edge on top.
          if marker_edge_thickness is not None and marker_edge_thickness > 0:
            cv2.rectangle(self._img, topleft, bottomright, 
                          marker_edge_color_bgr, marker_edge_thickness) # -1 fills the shape
        if marker_symbols[i].lower() == 'triangle':
          top = [x_i, int(y_i - np.ceil(marker_size/2))]
          bottomleft =  [int(x_i - np.ceil(marker_size/2)), int(y_i + np.ceil(marker_size/2))]
          bottomright = [int(x_i + np.ceil(marker_size/2)), int(y_i + np.ceil(marker_size/2))]
          # Draw the filled marker.
          cv2.drawContours(self._img, [np.array([bottomleft, top, bottomright])], 0, color_bgr, -1) # -1 fills the shape
          # Draw the edge on top.
          if marker_edge_thickness is not None and marker_edge_thickness > 0:
            cv2.drawContours(self._img, [np.array([bottomleft, top, bottomright])], 0, 
                             marker_edge_color_bgr, marker_edge_thickness)
        if marker_symbols[i].lower() == 'diamond':
          top = [x_i, int(y_i - np.ceil(marker_size/2))]
          bottom = [x_i, int(y_i + np.ceil(marker_size/2))]
          left =  [int(x_i - np.ceil(marker_size/2)), y_i]
          right =  [int(x_i + np.ceil(marker_size/2)), y_i]
          # Draw the filled marker.
          cv2.drawContours(self._img, [np.array([left, top, right, bottom])], 0, color_bgr, -1) # -1 fills the shape
          # Draw the edge on top.
          if marker_edge_thickness is not None and marker_edge_thickness > 0:
            cv2.drawContours(self._img, [np.array([left, top, right, bottom])], 0, 
                             marker_edge_color_bgr, marker_edge_thickness)
  
  # Add an image to the plot.
  # For example, may be a heatmap.
  # Will scale the image to fit the plot between the specified x and y limits.
  #  Will ignore the image aspect ratio to make it fill the specified limits.
  # If x and y limits of the image are omitted, will use the x and y limits of the plot.
  def plot_image(self, img, img_x_limits=None, img_y_limits=None, flip_image_upDown=False):
    img_x_limits = img_x_limits or self._xlim
    img_y_limits = img_y_limits or self._ylim
    # Scale the image.
    (left, bottom) = self._coordinates_to_pixels(min(img_x_limits), min(img_y_limits))
    (right, top) = self._coordinates_to_pixels(max(img_x_limits), max(img_y_limits))
    img_scaled = scale_image(img, target_width=(right-left)+1, target_height=(bottom-top)+1, 
                                  maintain_aspect_ratio=False)
    # Copy the image into the plot.
    # Flip it up/down if desired.
    #  Use reverse slicing to flip the image instead of np.flipud() since it may avoid an extra matrix copy.
    if flip_image_upDown:
      if top == 0:
        self._img[bottom::-1, left:(right+1), :] = img_scaled
      else:
        self._img[bottom:(top-1):-1, left:(right+1), :] = img_scaled
    else:
      self._img[top:(bottom+1), left:(right+1), :] = img_scaled
  
  # Get the rendered plot image.
  # Will be in RGB format.
  def get_plot_image(self):
    return cv2.cvtColor(self._img, cv2.COLOR_BGR2RGB)
  
  # Show the rendered plot.
  def show_plot(self, window_title='Woohoo! It plotted!', block=False):
    cv2.imshow(window_title, self._img)
    cv2.waitKey(0 if block else 1)
    
    




#########################################
# Testing
#########################################
if __name__ == '__main__':
  # Create a plot and configure it.
  plt = ImagePlot()
  plt.set_plot_size(width=int(600*4), height=int(600//(1+7/9)))
  # plt.set_axis_left_position(width_ratio=0.2)
  # plt.set_axis_right_position(width_ratio=0.8)
  # plt.set_padding(left=0, top=5, right=0, bottom=5)
  plt.set_padding(left=5, top=5, right=5, bottom=5)
  # plt.set_equal_aspect_ratio(True)
  plt.set_x_limits([0, 12])
  plt.set_y_limits([0, 12])
  plt.set_x_label('My Awesome X Label [units!]')
  plt.set_y_label('My Y Label [units!]')
  # plt.set_x_ticks_major([-1, 0, 2, 4, 6, 10])
  # plt.set_y_ticks_major([0, 2, 4, 6, 10])
  # plt.set_x_ticks_minor([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
  # plt.set_y_ticks_minor([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
  plt.set_x_ticks_spacing_major(2.5, value_to_include=0)
  plt.set_x_ticks_spacing_minor(1, value_to_include=0)
  plt.set_y_ticks_spacing_major(6)
  plt.set_y_ticks_spacing_minor(2)
  # plt.set_x_tick_label_format('%d')
  # plt.set_y_tick_label_format('%d')
  plt.show_tick_labels(x=True, y=True)
  plt.show_grid_major(x=True, y=True, thickness=1)
  plt.show_grid_minor(x=True, y=True, thickness=1)
  plt.show_box(False)
  plt.set_font_size(size=0.8, yLabelHeightRatio=None)
  plt.set_font_color((200, 0, 0))
  colormap = pyqtgraph.colormap.get('gist_stern', source='matplotlib', skipCache=True)
  color_lookup = colormap.getLookupTable(start=0, stop=1, nPts=plt.get_colorbar_area_height())
  plt.add_colorbar(color_lookup, 
                   width=30, limits=[0, 100], ticks=[10, 50, 90], 
                   label='COLORS')
  plt.render_empty()
  # plt.show_empty_plot()
  
  # Plot lines and measure the speed.
  N = 1000
  img_random = 255*np.random.random((56, 455, 3))
  img_random[0:10, :, :] = 255 # mark the top to check proper orientation
  img_random[:, 0:10, :] = 255 # mark the left to check proper orientation
  durations_plot_lines_s = []
  durations_plot_images_s = []
  durations_clear_plot_s = []
  durations_get_plotImage_s = []
  t0 = time.time()
  for i in range(N):
    # Clear the plot.
    t00 = time.time()
    plt.clear_plot()
    durations_clear_plot_s.append(time.time() - t00)
    # Demonstrate showing an image on the plot.
    t00 = time.time()
    plt.plot_image(img_random, (7, 10.5), (8, 10))
    durations_plot_images_s.append(time.time() - t00)
    # Demonstrate a vertical line.
    t00 = time.time()
    plt.plot(x=[0.5, 0.5], y=[0, 12], 
             line_thickness=2, 
             color=(0, 255, 0), 
             marker_symbols=None)
    durations_plot_lines_s.append(time.time() - t00)
    # Demonstrate a line marked with circles.
    t00 = time.time()
    plt.plot(x=[1, 2, 3, 7], y=[1, 5, 4, 1],
             line_thickness=3,
             color=(255, 0, 255),
             marker_symbols='circle',
             marker_size=15, marker_edge_thickness=0, marker_edge_color=(255, 255, 255))
    durations_plot_lines_s.append(time.time() - t00)
    # Demonstrate a line marked with squares.
    t00 = time.time()
    plt.plot(x=[1, 2, 3, 7], y=[2, 6, 5, 2],
             line_thickness=2,
             color=(255, 255, 0),
             marker_symbols='square',
             marker_size=10, marker_edge_thickness=0, marker_edge_color=(255, 255, 255))
    durations_plot_lines_s.append(time.time() - t00)
    # Demonstrate a line marked with triangles.
    t00 = time.time()
    plt.plot(x=[1, 2, 3, 7], y=[3, 7, 6, 3],
             line_thickness=1,
             color=(0, 255, 255),
             marker_symbols='triangle',
             marker_size=10, marker_edge_thickness=2, marker_edge_color=(255, 0, 255))
    durations_plot_lines_s.append(time.time() - t00)
    # Demonstrate a line marked with diamonds.
    t00 = time.time()
    plt.plot(x=[1, 2, 3, 7], y=[4, 8, 7, 4],
             line_thickness=3,
             color=(0, 0, 255),
             marker_symbols='diamond',
             marker_size=15, marker_edge_thickness=2, marker_edge_color=(0, 0, 255))
    durations_plot_lines_s.append(time.time() - t00)
    # Demonstrate a line marked with circles except for the last point which is a diamond.
    t00 = time.time()
    plt.plot(x=[1, 2, 3, 7], y=[6, 10, 9, 5],
             line_thickness=3,
             color=(255, 255, 255),
             marker_symbols=['circle']*3 + ['diamond'],
             marker_size=15, marker_edge_thickness=2, marker_edge_color=(150, 150, 150))
    durations_plot_lines_s.append(time.time() - t00)
    # Demonstrate a line that goes outside the axis limits.
    t00 = time.time()
    plt.plot(x=[-1,  5,   8, 9.5, 11, 15],
             y=[11, 11.8, 11, -2, 11, 10],
             line_thickness=3,
             color=(255, 0, 0),
             marker_symbols='circle',
             marker_size=15, marker_edge_thickness=2, marker_edge_color=(150, 150, 150))
    durations_plot_lines_s.append(time.time() - t00)
    # Demonstrate a single point.
    t00 = time.time()
    plt.plot(x=[11], y=[1],
             line_thickness=3,
             color=(255, 255, 255),
             marker_symbols='circle',
             marker_size=25, marker_edge_thickness=5, marker_edge_color=(150, 150, 150))
    durations_plot_lines_s.append(time.time() - t00)
    # Get the rendered plot image.
    t00 = time.time()
    img = plt.get_plot_image()
    durations_get_plotImage_s.append(time.time() - t00)
  
  # Print timing results.
  duration_s = time.time() - t0
  print('Timing results:')
  print('  Iterations    : %d' % N)
  print('  Total         : %7.2f Hz (%7.2f ms)' % (duration_s*1000, N/duration_s))
  print('  Plot a line   : %7.2f Hz (%7.2f ms)' % (1/np.mean(durations_plot_lines_s), np.mean(durations_plot_lines_s)*1000))
  print('  Add an image  : %7.2f Hz (%7.2f ms)' % (1/np.mean(durations_plot_images_s), np.mean(durations_plot_images_s)*1000))
  print('  Clear plot    : %7.2f Hz (%7.2f ms)' % (1/np.mean(durations_clear_plot_s), np.mean(durations_clear_plot_s)*1000))
  print('  Get plot image: %7.2f Hz (%7.2f ms)' % (1/np.mean(durations_get_plotImage_s), np.mean(durations_get_plotImage_s)*1000))
  print()
  
  # Save the plot image.
  cv2.imwrite('test_plot.jpg', img)
  
  # Show the final plot image.
  plt.show_plot(block=True)
  