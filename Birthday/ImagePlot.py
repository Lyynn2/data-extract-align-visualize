
import cv2
import numpy as np
import time
import pyqtgraph
from helpers import *

class ImagePlot:
  
  def __init__(self, auto_update_empty_plot=True):
    self._plot_size = [480, 640]
    self._auto_update_empty_plot = auto_update_empty_plot
    self._xlabel = ''
    self._ylabel = ''
    self._xlim = [0, 10]
    self._ylim = [0, 10]
    self._equal_aspect_ratio = False
    self._x_tick_spacing = {'major': 1, 'minor': 1}
    self._y_tick_spacing = {'major': 1, 'minor': 1}
    self._x_tick_value_to_include = 0
    self._y_tick_value_to_include = 0
    self._xticks = {'major': [], 'minor': []}
    self._yticks = {'major': [], 'minor': []}
    self._show_tick_labels_x = True
    self._show_tick_labels_y = True
    self._x_tick_label_format = '%g'
    self._y_tick_label_format = '%g'
    self._show_grid_x = {'major':True, 'minor':False}
    self._show_grid_y = {'major':True, 'minor':False}
    self._show_box = True
    self._grid_thickness = {'major':2, 'minor':2}
    self._grid_color = {'major':(125, 125, 125), 'minor':(50, 50, 50)}
    self._box_thickness = 2
    self._box_color = (200, 200, 200)
    self._text_bg_color = (0,0,0)
    self._text_color = (150, 150, 150)
    self._font_scale_ylabelHeightRatio = 0.3
    self._font_scale = None
    self._font_thickness = 1
    self._padding_left = 0
    self._padding_top = 0
    self._padding_right = 0
    self._padding_bottom = 0
    self._axis_left_position_widthRatio = None
    self._axis_right_position_widthRatio = None
    self._colorbar_img = None
    self._colorbar_pad_to_axis = None
    self._img_empty = None
    self._img = None
    self.render_empty()
    self.clear_plot()
  
  def set_plot_size(self, width, height):
    self._plot_size = [height, width]
  def set_padding(self, left, top, right, bottom):
    self._padding_left = int(left)
    self._padding_top = int(top)
    self._padding_right = int(right)
    self._padding_bottom = int(bottom)
    if self._auto_update_empty_plot:
      self.render_empty()
  def set_axis_left_position(self, width_ratio):
    self._axis_left_position_widthRatio = width_ratio
    if self._auto_update_empty_plot:
      self.render_empty()
  def set_axis_right_position(self, width_ratio):
    self._axis_right_position_widthRatio = width_ratio
    if self._auto_update_empty_plot:
      self.render_empty()
  
  def set_equal_aspect_ratio(self, equal_aspect_ratio):
    self._equal_aspect_ratio = equal_aspect_ratio
    # Adjust the current limits to enforce an equal aspect ratio.
    if self._equal_aspect_ratio:
      if self._axis_size[0] > self._axis_size[1]:
        self.set_x_limits(self._xlim)
      else:
        self.set_y_limits(self._ylim)
    
  def set_x_limits(self, limits):
    old_limits = self._xlim
    self._xlim = limits
    if self._equal_aspect_ratio:
      self.render_empty()
      y_ratio = self._axis_size[0]/self._axis_size[1]
      yrange = (self._xlim[1] - self._xlim[0])*y_ratio
      ycenter = np.mean(self._ylim)
      self._ylim = ycenter + np.array([-1, 1])*yrange/2
    if self._auto_update_empty_plot and np.any(old_limits != self._xlim):
      self.render_empty()
  def set_y_limits(self, limits):
    old_limits = self._ylim
    self._ylim = limits
    if self._equal_aspect_ratio:
      self.render_empty()
      x_ratio = self._axis_size[1]/self._axis_size[0]
      xrange = (self._ylim[1] - self._ylim[0])*x_ratio
      xcenter = np.mean(self._xlim)
      self._xlim = xcenter + np.array([-1, 1])*xrange/2
    if self._auto_update_empty_plot and np.any(old_limits != self._ylim):
      self.render_empty()
  def get_x_limits(self):
    return self._xlim
  def get_y_limits(self):
    return self._ylim
  def get_x_range(self):
    return self._xlim[1] - self._xlim[0]
  def get_y_range(self):
    return self._ylim[1] - self._ylim[0]
    
  def set_x_label(self, label):
    self._xlabel = label
    if self._auto_update_empty_plot:
      self.render_empty()
  def set_y_label(self, label):
    self._ylabel = label
    if self._auto_update_empty_plot:
      self.render_empty()
  
  def set_x_ticks_spacing(self, major, minor, value_to_include=0):
    self.set_x_ticks_spacing_major(major, value_to_include)
    self.set_x_ticks_spacing_minor(minor, value_to_include)
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
  def set_y_ticks_spacing(self, major, minor, value_to_include=0):
    self.set_y_ticks_spacing_major(major, value_to_include)
    self.set_y_ticks_spacing_minor(minor, value_to_include)
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
    
  def set_x_ticks_major(self, ticks):
    self._xticks['major'] = ticks
    if ticks is not None:
      self._x_tick_spacing['major'] = None # use manual ticks instead of auto
    if self._auto_update_empty_plot:
      self.render_empty()
  def set_x_ticks_minor(self, ticks):
    self._xticks['minor'] = ticks
    if ticks is not None:
      self._x_tick_spacing['minor'] = None # use manual ticks instead of auto
    if self._auto_update_empty_plot:
      self.render_empty()
  def set_y_ticks_major(self, ticks):
    self._yticks['major'] = ticks
    if ticks is not None:
      self._y_tick_spacing['major'] = None # use manual ticks instead of auto
    if self._auto_update_empty_plot:
      self.render_empty()
  def set_y_ticks_minor(self, ticks):
    self._yticks['minor'] = ticks
    if ticks is not None:
      self._y_tick_spacing['minor'] = None # use manual ticks instead of auto
    if self._auto_update_empty_plot:
      self.render_empty()
  
  def show_tick_labels(self, x=True, y=True):
    self._show_tick_labels_x = x
    self._show_tick_labels_y = y
    if self._auto_update_empty_plot:
      self.render_empty()
  
  def set_x_tick_label_format(self, format_str):
    self._x_tick_label_format = format_str
  def set_y_tick_label_format(self, format_str):
    self._y_tick_label_format = format_str
    
  def show_grid_major(self, x=True, y=True, color=None, thickness=None):
    self._show_grid_x['major'] = x
    self._show_grid_y['major'] = y
    self._grid_color['major'] = color or self._grid_color['major']
    self._grid_thickness['major'] = thickness or self._grid_thickness['major']
    if self._auto_update_empty_plot:
      self.render_empty()
  def show_grid_minor(self, x=True, y=True, color=None, thickness=None):
    self._show_grid_x['minor'] = x
    self._show_grid_y['minor'] = y
    self._grid_color['minor'] = color or self._grid_color['minor']
    self._grid_thickness['minor'] = thickness or self._grid_thickness['minor']
    if self._auto_update_empty_plot:
      self.render_empty()
  def show_box(self, show, color=None, thickness=None):
    self._show_box = show
    self._box_color = color or self._box_color
    self._box_thickness = thickness or self._box_thickness
    if self._auto_update_empty_plot:
      self.render_empty()
    
  def set_font_size(self, size=None, yLabelHeightRatio=None, thickness=1):
    if size is not None:
      self._font_scale = size
      self._font_scale_ylabelHeightRatio = None
    if yLabelHeightRatio is not None:
      self._font_scale_ylabelHeightRatio = yLabelHeightRatio
      self._font_scale = None
    self._font_thickness = thickness
    if self._auto_update_empty_plot:
      self.render_empty()
    
  def set_font_color(self, color):
    self._text_color = color
    if self._auto_update_empty_plot:
      self.render_empty()
  
  def add_colorbar(self, colormap, width, limits, ticks=None,
                   label='',
                   pad_to_axis=10, label_padding=5,
                   tick_label_format='%g'):
    if ticks is None:
      ticks = []
    
    # Determine the size of the area for the colorbar.
    self.render_empty()
    bottom = int(self._axis_bottomleft_position[0])
    top = int(self._axis_bottomleft_position[0] - self._axis_size[0])
    height = int((bottom - top) + 1)
    
    # Determine size of tick labels and of main label.
    tick_labels = [tick_label_format % tick for tick in ticks]
    temp_img = self._img_empty.copy()
    tick_dims = [draw_text_on_image(temp_img, tick_label, pos=(0.5, 0.5),
                                       text_width_ratio=None, font_scale=self._font_scale,
                                       font_thickness=self._font_thickness, font=cv2.FONT_HERSHEY_DUPLEX,
                                       text_color=self._text_color, text_bg_color=self._text_bg_color, text_bg_outline_color=None, text_bg_pad_width_ratio=0,
                                       preview_only=True,
                                       ) for tick_label in tick_labels]
    tick_widths = [int(w) for (w, h, f) in tick_dims]
    tick_heights = [int(h) for (w, h, f) in tick_dims]
    if len(label) > 0:
      label_font_scale = self._font_scale
      label_dims = draw_text_on_image(temp_img, label, pos=(0.5, 0.5),
                                       text_width_ratio=None, font_scale=label_font_scale,
                                       font_thickness=self._font_thickness, font=cv2.FONT_HERSHEY_DUPLEX,
                                       text_color=self._text_color, text_bg_color=self._text_bg_color, text_bg_outline_color=None, text_bg_pad_width_ratio=0,
                                       preview_only=True,
                                       )
      if label_dims[0] > height:
        label_dims = draw_text_on_image(temp_img, label, pos=(0.5, 0.5),
                                         text_width_ratio=0.95, font_scale=None,
                                         font_thickness=self._font_thickness, font=cv2.FONT_HERSHEY_DUPLEX,
                                         text_color=self._text_color, text_bg_color=self._text_bg_color, text_bg_outline_color=None, text_bg_pad_width_ratio=0,
                                         preview_only=True,
                                         )
      (label_width, label_height, label_font_scale) = label_dims
    else:
      (label_width, label_height) = (0, 0)
    label_height = int(label_height*2.0)
    
    # Create an image of the appropriate size.
    img_width =  width + label_padding + max(tick_widths)
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
      draw_text_on_image(img, tick_label, pos=(x, y),
                                       text_width_ratio=None, font_scale=self._font_scale,
                                       font_thickness=self._font_thickness, font=cv2.FONT_HERSHEY_DUPLEX,
                                       text_color=self._text_color, text_bg_color=self._text_bg_color, text_bg_outline_color=None, text_bg_pad_width_ratio=0,
                                       preview_only=False,
                                       )
    # Add the main label.
    if len(label) > 0:
      label_img = np.zeros(shape=(label_height, height, 3), dtype=np.uint8)
      draw_text_on_image(label_img, label, pos=(0.5, 0.5),
                         text_width_ratio=None, font_scale=label_font_scale,
                         font_thickness=self._font_thickness, font=cv2.FONT_HERSHEY_DUPLEX,
                         text_color=self._text_color, text_bg_color=self._text_bg_color, text_bg_outline_color=None, text_bg_pad_width_ratio=0,
                         preview_only=False,
                         )
      label_img = np.flipud(np.transpose(label_img, axes=[1,0,2]))
      img[:, (img_width-label_height):(img_width+1), :] = label_img
    
    # Add colors.
    color_lookup = colormap.getLookupTable(start=0, stop=1, nPts=height)
    # color_lookup_keys = np.linspace(start=limits[0], stop=limits[1], num=height)
    for y in range(height):
      img[(height-1)-y, 0:width, :] = np.flip(color_lookup[y])
    
    # Store result.
    self._colorbar_img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    self._colorbar_pad_to_axis = int(pad_to_axis)
    self.set_equal_aspect_ratio(self._equal_aspect_ratio) # update limits since the axis aspect ratio has changed to fit the colorbar
    self.render_empty()
  
  def render_empty(self):
    top_pad = np.ceil(self._box_thickness/2) + self._padding_top
    right_pad = np.ceil(self._box_thickness/2) + self._padding_right
    left_pad =  self._padding_left
    bottom_pad =  self._padding_bottom
    
    self._img_empty = np.zeros(shape=(*self._plot_size, 3), dtype=np.uint8)
    # Determine the size of the ylabel,
    #  and if desired determine a font scale that will make the y label fit nicely.
    temp_img = np.zeros(shape=(self._plot_size[1], self._plot_size[0], 3), dtype=np.uint8)
    ylabel_width, ylabel_height, font_scale = draw_text_on_image(temp_img, self._ylabel, pos=(0, 0),
                                               text_width_ratio=self._font_scale_ylabelHeightRatio, font_scale=self._font_scale,
                                               font_thickness=self._font_thickness, font=cv2.FONT_HERSHEY_DUPLEX,
                                               text_color=self._text_color, text_bg_color=self._text_bg_color, text_bg_outline_color=None, text_bg_pad_width_ratio=0,
                                               preview_only=True,
                                               )
    if ylabel_width > self._plot_size[0]*0.9:
      ylabel_width, ylabel_height, font_scale = draw_text_on_image(temp_img, self._ylabel, pos=(0, 0),
                                                 text_width_ratio=0.9, font_scale=None,
                                                 font_thickness=self._font_thickness, font=cv2.FONT_HERSHEY_DUPLEX,
                                                 text_color=self._text_color, text_bg_color=self._text_bg_color, text_bg_outline_color=None, text_bg_pad_width_ratio=0,
                                                 preview_only=True,
                                                 )
    self._font_scale = font_scale
    if len(self._ylabel) > 0:
      ylabel_height = round(ylabel_height*2.0) # account for undershoot under the text baseline
      # Create an image with the y label text.
      ylabel_img = np.zeros(shape=(ylabel_height, ylabel_width, 3), dtype=np.uint8)
      draw_text_on_image(ylabel_img, self._ylabel, pos=(0.5, 0.5),
                         text_width_ratio=None, font_scale=self._font_scale,
                         font_thickness=self._font_thickness, font=cv2.FONT_HERSHEY_DUPLEX,
                         text_color=self._text_color, text_bg_color=self._text_bg_color, text_bg_outline_color=None, text_bg_pad_width_ratio=0,
                         preview_only=False,
                         )
      ylabel_img = np.flipud(np.transpose(ylabel_img, axes=[1,0,2]))
    else:
      ylabel_width = 0
      ylabel_height = 0
    # Create an image with the x label text.
    temp_img = np.zeros(shape=(self._plot_size[0], self._plot_size[1], 3), dtype=np.uint8)
    xlabel_width, xlabel_height, _ = draw_text_on_image(temp_img, self._xlabel, pos=(0, 0),
                                                        text_width_ratio=None, font_scale=self._font_scale,
                                                        font_thickness=self._font_thickness, font=cv2.FONT_HERSHEY_DUPLEX,
                                                        text_color=self._text_color, text_bg_color=self._text_bg_color, text_bg_outline_color=None, text_bg_pad_width_ratio=0,
                                                        preview_only=True,
                                                        )
    if xlabel_width > self._plot_size[1]*0.9:
      xlabel_width, xlabel_height, font_scale = draw_text_on_image(temp_img, self._xlabel, pos=(0, 0),
                                                        text_width_ratio=0.9, font_scale=None,
                                                        font_thickness=self._font_thickness, font=cv2.FONT_HERSHEY_DUPLEX,
                                                        text_color=self._text_color, text_bg_color=self._text_bg_color, text_bg_outline_color=None, text_bg_pad_width_ratio=0,
                                                        preview_only=True,
                                                        )
      self._font_scale = font_scale
    if len(self._xlabel) > 0:
      xlabel_height = round(xlabel_height*2) # account for undershoot under the text baseline
      xlabel_img = np.zeros(shape=(xlabel_height, xlabel_width, 3), dtype=np.uint8)
      draw_text_on_image(xlabel_img, self._xlabel, pos=(0.5, 0.5),
                         text_width_ratio=None, font_scale=self._font_scale,
                         font_thickness=self._font_thickness, font=cv2.FONT_HERSHEY_DUPLEX,
                         text_color=self._text_color, text_bg_color=self._text_bg_color, text_bg_outline_color=None, text_bg_pad_width_ratio=0,
                         preview_only=False,
                         )
    else:
      xlabel_height = 0
      xlabel_width = 0
    
    # Determine tick locations based on manual locations or on spacing.
    for tick_type in ['minor', 'major']:
      if self._x_tick_spacing[tick_type] is not None:
        first_tick = next_multiple(self._xlim[0], self._x_tick_spacing[tick_type])
        last_tick = previous_multiple(self._xlim[1], self._x_tick_spacing[tick_type])
        self._xticks[tick_type] = np.linspace(start=first_tick, stop=last_tick,
                                              num=int(1+(last_tick - first_tick)/self._x_tick_spacing[tick_type]))
        offset_toAdd = self._x_tick_value_to_include - previous_multiple(self._x_tick_value_to_include, self._x_tick_spacing[tick_type])
        self._xticks[tick_type] += offset_toAdd
      if self._y_tick_spacing[tick_type] is not None:
        first_tick = next_multiple(self._ylim[0], self._y_tick_spacing[tick_type])
        last_tick = previous_multiple(self._ylim[1], self._y_tick_spacing[tick_type])
        self._yticks[tick_type] = np.linspace(start=first_tick, stop=last_tick,
                                              num=int(1+(last_tick - first_tick)/self._y_tick_spacing[tick_type]))
        offset_toAdd = self._y_tick_value_to_include - previous_multiple(self._y_tick_value_to_include, self._y_tick_spacing[tick_type])
        self._yticks[tick_type] += offset_toAdd
    
    # Determine sizes of the tick labels.
    xtick_labels = [self._x_tick_label_format % tick for tick in self._xticks['major']]
    ytick_labels = [self._y_tick_label_format % tick for tick in self._yticks['major']]
    xtick_dims = [draw_text_on_image(temp_img, xtick_label, pos=(0, 0),
                                       text_width_ratio=None, font_scale=self._font_scale,
                                       font_thickness=self._font_thickness, font=cv2.FONT_HERSHEY_DUPLEX,
                                       text_color=self._text_color, text_bg_color=self._text_bg_color, text_bg_outline_color=None, text_bg_pad_width_ratio=0,
                                       preview_only=True,
                                       ) for xtick_label in xtick_labels]
    xtick_widths = [w for (w, h, f) in xtick_dims]
    xtick_heights = [round(h*1.0) for (w, h, f) in xtick_dims] # scale to account for undershoot under the text baseline
    if not self._show_tick_labels_x:
      xtick_widths = [0]*len(xtick_widths)
      xtick_heights = [0]*len(xtick_heights)
    xticks_height = max(xtick_heights)
    ytick_dims = [draw_text_on_image(temp_img, ytick_label, pos=(0, 0),
                                       text_width_ratio=None, font_scale=self._font_scale,
                                       font_thickness=self._font_thickness, font=cv2.FONT_HERSHEY_DUPLEX,
                                       text_color=self._text_color, text_bg_color=self._text_bg_color, text_bg_outline_color=None, text_bg_pad_width_ratio=0,
                                       preview_only=True,
                                       ) for ytick_label in ytick_labels]
    ytick_widths = [w for (w, h, f) in ytick_dims]
    ytick_heights = [round(h*1.0) for (w, h, f) in ytick_dims]  # scale to account for undershoot under the text baseline
    if not self._show_tick_labels_y:
      ytick_widths = [0]*len(ytick_widths)
      ytick_heights = [0]*len(ytick_heights)
    yticks_width = max(ytick_widths)
    
    # Determine size of labels and ticks, with padding.
    ylabel_height_padded = ylabel_height + max(2.0, ylabel_height*0.1)
    ylabel_width_padded = ylabel_width + max(2.0, ylabel_width*0.1)
    xlabel_height_padded = xlabel_height + max(2.0, xlabel_height*0.1)
    xlabel_width_padded = xlabel_width + max(2.0, xlabel_width*0.1)
    xticks_height_padded = xticks_height + max([2.0, xticks_height*0.5])
    yticks_width_padded = yticks_width + max([2.0, yticks_width*0.1])
    
    # Determine position and size of axis area.
    axis_x_left_offset = round(yticks_width_padded + ylabel_height_padded + left_pad + self._box_thickness/2)
    axis_y_bottom_offset = round(xticks_height_padded + xlabel_height_padded + bottom_pad + self._box_thickness/2)
    axis_y_top_offset = top_pad
    axis_x_right_offset = right_pad
    if self._colorbar_img is not None:
      axis_x_right_offset += self._colorbar_img.shape[1] + self._colorbar_pad_to_axis
    self._axis_bottomleft_position = [self._plot_size[0] - axis_y_bottom_offset, axis_x_left_offset]
    self._axis_size = [self._plot_size[0] - axis_y_bottom_offset - axis_y_top_offset,
                       self._plot_size[1] - axis_x_left_offset - axis_x_right_offset]
    # Override if desired.
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
      temp_img = np.zeros(shape=(self._axis_size[0], self._axis_size[1], 3), dtype=np.uint8)
      xlabel_width, xlabel_height, font_scale = draw_text_on_image(temp_img, self._xlabel, pos=(0, 0),
                                                        text_width_ratio=0.99, font_scale=None,
                                                        font_thickness=self._font_thickness, font=cv2.FONT_HERSHEY_DUPLEX,
                                                        text_color=self._text_color, text_bg_color=self._text_bg_color, text_bg_outline_color=None, text_bg_pad_width_ratio=0,
                                                        preview_only=True,
                                                        )
      self._font_scale = font_scale
    if ylabel_width > self._axis_size[0]:
      temp_img = np.zeros(shape=(self._axis_size[1], self._axis_size[0], 3), dtype=np.uint8)
      ylabel_width, ylabel_height, font_scale = draw_text_on_image(temp_img, self._ylabel, pos=(0, 0),
                                                 text_width_ratio=0.99, font_scale=None,
                                                 font_thickness=self._font_thickness, font=cv2.FONT_HERSHEY_DUPLEX,
                                                 text_color=self._text_color, text_bg_color=self._text_bg_color, text_bg_outline_color=None, text_bg_pad_width_ratio=0,
                                                 preview_only=True,
                                                 )
      self._font_scale = font_scale
      ylabel_height = round(ylabel_height*2.0) # account for undershoot under the text baseline
      # Create an image with the y label text.
      ylabel_img = np.zeros(shape=(ylabel_height, ylabel_width, 3), dtype=np.uint8)
      draw_text_on_image(ylabel_img, self._ylabel, pos=(0.5, 0.5),
                         text_width_ratio=None, font_scale=self._font_scale,
                         font_thickness=self._font_thickness, font=cv2.FONT_HERSHEY_DUPLEX,
                         text_color=self._text_color, text_bg_color=self._text_bg_color, text_bg_outline_color=None, text_bg_pad_width_ratio=0,
                         preview_only=False,
                         )
      ylabel_img = np.flipud(np.transpose(ylabel_img, axes=[1,0,2]))
      
    # Add the y axis label to the empty image.
    # It will be centered to the axis area.
    if len(self._ylabel) > 0:
      ylabel_center_x = self._axis_bottomleft_position[1] - yticks_width_padded - ylabel_height_padded//2
      ylabel_center_y = self._axis_bottomleft_position[0] - self._axis_size[0]/2
      ylabel_top_y = round(ylabel_center_y - ylabel_width/2)
      ylabel_bottom_y = ylabel_top_y + ylabel_width - 1
      ylabel_left_x = round(ylabel_center_x - ylabel_height/2)
      ylabel_right_x = ylabel_left_x + ylabel_height - 1
      self._img_empty[ylabel_top_y:(ylabel_bottom_y+1), ylabel_left_x:(ylabel_right_x+1), :] = ylabel_img
    
    # Add the x axis label to the empty image.
    # It will be centered to the axis area.
    if len(self._xlabel) > 0:
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
                           font_thickness=self._font_thickness, font=cv2.FONT_HERSHEY_DUPLEX,
                           text_color=self._text_color, text_bg_color=self._text_bg_color, text_bg_outline_color=None, text_bg_pad_width_ratio=0,
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
        draw_text_on_image(self._img_empty, label, pos=(ticklabel_left_x, ticklabel_top_y),
                           text_width_ratio=None, font_scale=self._font_scale,
                           font_thickness=self._font_thickness, font=cv2.FONT_HERSHEY_DUPLEX,
                           text_color=self._text_color, text_bg_color=self._text_bg_color, text_bg_outline_color=None, text_bg_pad_width_ratio=0,
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
          cv2.line(self._img_empty, bottom_pos, top_pos, self._grid_color[grid_type], self._grid_thickness[grid_type])
      if self._show_grid_y[grid_type]:
        for (tick_index, y) in enumerate(self._yticks[grid_type]):
          if y < self._ylim[0] or y > self._ylim[1]:
            continue
          left_pos = self._coordinates_to_pixels(x=self._xlim[0], y=y)
          right_pos = self._coordinates_to_pixels(x=self._xlim[1], y=y)
          cv2.line(self._img_empty, left_pos, right_pos, self._grid_color[grid_type], self._grid_thickness[grid_type])
      
    # Get positions of axis
    bottomleft_pos = self._coordinates_to_pixels(x=self._xlim[0], y=self._ylim[0])
    bottomright_pos = self._coordinates_to_pixels(x=self._xlim[1], y=self._ylim[0])
    topleft_pos = self._coordinates_to_pixels(x=self._xlim[0], y=self._ylim[1])
    topright_pos = self._coordinates_to_pixels(x=self._xlim[1], y=self._ylim[1])
    
    # Add bottom and left axes lines.
    cv2.line(self._img_empty, bottomleft_pos, bottomright_pos, self._box_color, self._box_thickness)
    cv2.line(self._img_empty, bottomleft_pos, topleft_pos, self._box_color, self._box_thickness)
    
    # Add bottom and left lines of axis.
    cv2.line(self._img_empty, bottomleft_pos, bottomright_pos, self._box_color, self._box_thickness)
    cv2.line(self._img_empty, bottomleft_pos, topleft_pos, self._box_color, self._box_thickness)
    
    # Add box if desired.
    if self._show_box:
      cv2.line(self._img_empty, topleft_pos, topright_pos, self._box_color, self._box_thickness)
      cv2.line(self._img_empty, bottomright_pos, topright_pos, self._box_color, self._box_thickness)
      
    # Add colorbar if desired.
    if self._colorbar_img is not None:
      left = int(self._axis_bottomleft_position[1] + self._axis_size[1] + self._colorbar_pad_to_axis)
      right = int(left + self._colorbar_img.shape[1] - 1)
      bottom = int(self._axis_bottomleft_position[0])
      top = int(bottom - (self._colorbar_img.shape[0] - 1))
      self._img_empty[top:(bottom+1), left:(right+1), :] = self._colorbar_img
    
  def show_empty_plot(self, window_title='Great emptiness!', block=False):
    self.render_empty()
    img = self._img_empty
    cv2.imshow(window_title, img)
    cv2.waitKey(0 if block else 1)
    
  def _coordinates_to_pixels(self, x, y):
    x_fraction = (x - self._xlim[0]) / (self._xlim[1] - self._xlim[0])
    y_fraction = (y - self._ylim[0]) / (self._ylim[1] - self._ylim[0])
    x_pixel = round(self._axis_bottomleft_position[1] + self._axis_size[1] * x_fraction)
    y_pixel = round(self._axis_bottomleft_position[0] - self._axis_size[0] * y_fraction)
    return (x_pixel, y_pixel)
  
  def clear_plot(self):
    self._img = self._img_empty.copy()
  
  def get_plot_image(self):
    return cv2.cvtColor(self._img, cv2.COLOR_BGR2RGB)

  def show_plot(self, window_title='Woohoo! It plotted!', block=False):
    img = self._img
    cv2.imshow(window_title, img)
    cv2.waitKey(0 if block else 1)
  
  def plot_line(self, x, y,
                line_thickness=1,
                color=(255, 255, 255),
                marker_symbols='circle',
                marker_size=2, marker_edge_thickness=0, marker_edge_color=(255, 255, 255)):
    if not isinstance(x, (list, tuple, np.ndarray)):
      x = [x]
    if not isinstance(y, (list, tuple, np.ndarray)):
      y = [y]
    if isinstance(color, np.ndarray):
      color = color.tolist()
    if isinstance(marker_edge_color, np.ndarray):
      marker_edge_color = marker_edge_color.tolist()
    # Draw the lines.
    if len(x) > 1:
      for i in range(1,len(x)):
        # TODO draw the line segment that intersects with the edge of the window instead of ignoring the out of bounds point
        if x[i] < self._xlim[0] or x[i-1] < self._xlim[0] or x[i] > self._xlim[1] or x[i-1] > self._xlim[1]:
          continue
        if y[i] < self._ylim[0] or y[i-1] < self._ylim[0] or y[i] > self._ylim[1] or y[i-1] > self._ylim[1]:
          continue
        (x_i, y_i) = self._coordinates_to_pixels(x[i], y[i])
        (x_iprev, y_iprev) = self._coordinates_to_pixels(x[i-1], y[i-1])
        cv2.line(self._img, (x_i, y_i), (x_iprev, y_iprev), color, line_thickness)
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
                     color=color, thickness=-1) # -1 fills the shape
          # Draw the edge on top.
          if marker_edge_thickness is not None and marker_edge_thickness > 0:
            cv2.circle(self._img, (x_i, y_i), radius=int(np.ceil(marker_size/2)),
                       color=marker_edge_color, thickness=marker_edge_thickness)
        if marker_symbols[i].lower() == 'square':
          topleft = [int(x_i - np.ceil(marker_size/2)), int(y_i - np.ceil(marker_size/2))]
          bottomright = [int(x_i + np.ceil(marker_size/2)), int(y_i + np.ceil(marker_size/2))]
          # Draw the filled marker.
          cv2.rectangle(self._img, topleft, bottomright,
                        color, -1) # -1 fills the shape
          # Draw the edge on top.
          if marker_edge_thickness is not None and marker_edge_thickness > 0:
            cv2.rectangle(self._img, topleft, bottomright,
                          marker_edge_color, marker_edge_thickness) # -1 fills the shape
        if marker_symbols[i].lower() == 'triangle':
          top = [x_i, int(y_i - np.ceil(marker_size/2))]
          bottomleft =  [int(x_i - np.ceil(marker_size/2)), int(y_i + np.ceil(marker_size/2))]
          bottomright = [int(x_i + np.ceil(marker_size/2)), int(y_i + np.ceil(marker_size/2))]
          # Draw the filled marker.
          cv2.drawContours(self._img, [np.array([bottomleft, top, bottomright])], 0, color, -1) # -1 fills the shape
          # Draw the edge on top.
          if marker_edge_thickness is not None and marker_edge_thickness > 0:
            cv2.drawContours(self._img, [np.array([bottomleft, top, bottomright])], 0,
                             marker_edge_color, marker_edge_thickness)
        if marker_symbols[i].lower() == 'diamond':
          top = [x_i, int(y_i - np.ceil(marker_size/2))]
          bottom = [x_i, int(y_i + np.ceil(marker_size/2))]
          left =  [int(x_i - np.ceil(marker_size/2)), y_i]
          right =  [int(x_i + np.ceil(marker_size/2)), y_i]
          # Draw the filled marker.
          cv2.drawContours(self._img, [np.array([left, top, right, bottom])], 0, color, -1) # -1 fills the shape
          # Draw the edge on top.
          if marker_edge_thickness is not None and marker_edge_thickness > 0:
            cv2.drawContours(self._img, [np.array([left, top, right, bottom])], 0,
                             marker_edge_color, marker_edge_thickness)
  
  def plot_image(self, img, img_x_limits=None, img_y_limits=None):
    img_x_limits = img_x_limits or self._xlim
    img_y_limits = img_y_limits or self._ylim
    (left, bottom) = self._coordinates_to_pixels(img_x_limits[0], img_y_limits[0])
    (right, top) = self._coordinates_to_pixels(img_x_limits[1], img_y_limits[1])
    img_scaled = scale_image(img, target_width=(right-left)+1, target_height=(bottom-top)+1,
                                  maintain_aspect_ratio=False)
    self._img[top:(bottom+1), left:(right+1), :] = np.flipud(img_scaled)
    
if __name__ == '__main__':
  plt = ImagePlot()
  plt.set_plot_size(width=int(300*4), height=int(600//(1+7/9)))
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
  plt.set_font_color((200, 200, 200))
  plt.add_colorbar(pyqtgraph.colormap.get('gist_stern', source='matplotlib', skipCache=True),
                   width=30, limits=[0,100], ticks=[10, 50, 90],
                   label='COLORS')
  plt.render_empty()
  
  N = 1000
  
  # t0 = time.time()
  # for i in range(N):
  #   plt.render_empty()
  # print(N/(time.time() - t0))
  # #plt.show_empty_plot()
  
  img_random = 255*np.random.random((56, 455, 3))
  
  t0 = time.time()
  for i in range(N):
    plt.clear_plot()
    plt.plot_line(x=[0.5, 0.5], y=[0, 12],
                    line_thickness=2,
                    color=(0, 255, 0),
                    marker_symbols=None)
    # for j in range(3):
    #   plt.plot_line(x=[1,2,3,7], y=[1,5,4,1],
    #                 line_thickness=3,
    #                 color=(255, 0, 255),
    #                 marker_symbols='circle',
    #                 marker_size=15, marker_edge_thickness=0, marker_edge_color=(255, 255, 255))
    #   plt.plot_line(x=[1,2,3,7], y=[2,6,5,2],
    #                 line_thickness=2,
    #                 color=(255, 255, 0),
    #                 marker_symbols='square',
    #                 marker_size=10, marker_edge_thickness=0, marker_edge_color=(255, 255, 255))
    #   plt.plot_line(x=[1,2,3,7], y=[3,7,6,3],
    #                 line_thickness=1,
    #                 color=(0, 255, 255),
    #                 marker_symbols='triangle',
    #                 marker_size=10, marker_edge_thickness=2, marker_edge_color=(255, 0, 255))
    #   plt.plot_line(x=[1,2,3,7], y=[4,8,7,4],
    #                 line_thickness=3,
    #                 color=(0, 0, 255),
    #                 marker_symbols='diamond',
    #                 marker_size=15, marker_edge_thickness=2, marker_edge_color=(0, 0, 255))
    #   plt.plot_line(x=[1,2,3,7], y=[6,10,9,5],
    #                 line_thickness=3,
    #                 color=(255, 255, 255),
    #                 marker_symbols=['circle']*3 + ['diamond'],
    #                 marker_size=15, marker_edge_thickness=2, marker_edge_color=(150, 150, 150))
    #   plt.plot_line(x=[11], y=[1],
    #                 line_thickness=3,
    #                 color=(255, 255, 255),
    #                 marker_symbols='circle',
    #                 marker_size=25, marker_edge_thickness=5, marker_edge_color=(150, 150, 150))
    plt.plot_image(img_random, (6, 11.8), (9,11))
    img = plt.get_plot_image()
  print(N/(time.time() - t0))
  cv2.imwrite('test_plot.jpg', img)
  
  plt.show_plot(block=True)