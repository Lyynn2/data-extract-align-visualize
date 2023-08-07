<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE eagle SYSTEM "eagle.dtd">
<eagle version="9.6.2">
<drawing>
<settings>
<setting alwaysvectorfont="no"/>
<setting verticaltext="up"/>
</settings>
<grid distance="0.1" unitdist="inch" unit="inch" style="lines" multiple="1" display="no" altdistance="0.01" altunitdist="inch" altunit="inch"/>
<layers>
<layer number="1" name="Top" color="4" fill="1" visible="no" active="no"/>
<layer number="2" name="Route2" color="1" fill="3" visible="no" active="no"/>
<layer number="3" name="Route3" color="4" fill="3" visible="no" active="no"/>
<layer number="4" name="Route4" color="1" fill="4" visible="no" active="no"/>
<layer number="5" name="Route5" color="4" fill="4" visible="no" active="no"/>
<layer number="6" name="Route6" color="1" fill="8" visible="no" active="no"/>
<layer number="7" name="Route7" color="4" fill="8" visible="no" active="no"/>
<layer number="8" name="Route8" color="1" fill="2" visible="no" active="no"/>
<layer number="9" name="Route9" color="4" fill="2" visible="no" active="no"/>
<layer number="10" name="Route10" color="1" fill="7" visible="no" active="no"/>
<layer number="11" name="Route11" color="4" fill="7" visible="no" active="no"/>
<layer number="12" name="Route12" color="1" fill="5" visible="no" active="no"/>
<layer number="13" name="Route13" color="4" fill="5" visible="no" active="no"/>
<layer number="14" name="Route14" color="1" fill="6" visible="no" active="no"/>
<layer number="15" name="Route15" color="4" fill="6" visible="no" active="no"/>
<layer number="16" name="Bottom" color="1" fill="1" visible="no" active="no"/>
<layer number="17" name="Pads" color="2" fill="1" visible="no" active="no"/>
<layer number="18" name="Vias" color="2" fill="1" visible="no" active="no"/>
<layer number="19" name="Unrouted" color="6" fill="1" visible="no" active="no"/>
<layer number="20" name="Dimension" color="15" fill="1" visible="no" active="no"/>
<layer number="21" name="tPlace" color="7" fill="1" visible="no" active="no"/>
<layer number="22" name="bPlace" color="7" fill="1" visible="no" active="no"/>
<layer number="23" name="tOrigins" color="15" fill="1" visible="no" active="no"/>
<layer number="24" name="bOrigins" color="15" fill="1" visible="no" active="no"/>
<layer number="25" name="tNames" color="7" fill="1" visible="no" active="no"/>
<layer number="26" name="bNames" color="7" fill="1" visible="no" active="no"/>
<layer number="27" name="tValues" color="7" fill="1" visible="no" active="no"/>
<layer number="28" name="bValues" color="7" fill="1" visible="no" active="no"/>
<layer number="29" name="tStop" color="7" fill="3" visible="no" active="no"/>
<layer number="30" name="bStop" color="7" fill="6" visible="no" active="no"/>
<layer number="31" name="tCream" color="7" fill="4" visible="no" active="no"/>
<layer number="32" name="bCream" color="7" fill="5" visible="no" active="no"/>
<layer number="33" name="tFinish" color="6" fill="3" visible="no" active="no"/>
<layer number="34" name="bFinish" color="6" fill="6" visible="no" active="no"/>
<layer number="35" name="tGlue" color="7" fill="4" visible="no" active="no"/>
<layer number="36" name="bGlue" color="7" fill="5" visible="no" active="no"/>
<layer number="37" name="tTest" color="7" fill="1" visible="no" active="no"/>
<layer number="38" name="bTest" color="7" fill="1" visible="no" active="no"/>
<layer number="39" name="tKeepout" color="4" fill="11" visible="no" active="no"/>
<layer number="40" name="bKeepout" color="1" fill="11" visible="no" active="no"/>
<layer number="41" name="tRestrict" color="4" fill="10" visible="no" active="no"/>
<layer number="42" name="bRestrict" color="1" fill="10" visible="no" active="no"/>
<layer number="43" name="vRestrict" color="2" fill="10" visible="no" active="no"/>
<layer number="44" name="Drills" color="7" fill="1" visible="no" active="no"/>
<layer number="45" name="Holes" color="7" fill="1" visible="no" active="no"/>
<layer number="46" name="Milling" color="3" fill="1" visible="no" active="no"/>
<layer number="47" name="Measures" color="7" fill="1" visible="no" active="no"/>
<layer number="48" name="Document" color="7" fill="1" visible="no" active="no"/>
<layer number="49" name="Reference" color="7" fill="1" visible="no" active="no"/>
<layer number="51" name="tDocu" color="7" fill="1" visible="no" active="no"/>
<layer number="52" name="bDocu" color="7" fill="1" visible="no" active="no"/>
<layer number="88" name="SimResults" color="9" fill="1" visible="yes" active="yes"/>
<layer number="89" name="SimProbes" color="9" fill="1" visible="yes" active="yes"/>
<layer number="90" name="Modules" color="5" fill="1" visible="yes" active="yes"/>
<layer number="91" name="Nets" color="2" fill="1" visible="yes" active="yes"/>
<layer number="92" name="Busses" color="1" fill="1" visible="yes" active="yes"/>
<layer number="93" name="Pins" color="2" fill="1" visible="no" active="yes"/>
<layer number="94" name="Symbols" color="4" fill="1" visible="yes" active="yes"/>
<layer number="95" name="Names" color="7" fill="1" visible="yes" active="yes"/>
<layer number="96" name="Values" color="7" fill="1" visible="yes" active="yes"/>
<layer number="97" name="Info" color="7" fill="1" visible="yes" active="yes"/>
<layer number="98" name="Guide" color="6" fill="1" visible="yes" active="yes"/>
</layers>
<schematic xreflabel="%F%N/%S.%C%R" xrefpart="/%S.%C%R">
<libraries>
<library name="Custom-Frames">
<description>&lt;b&gt;Frames for Sheet and Layout&lt;/b&gt;</description>
<packages>
</packages>
<symbols>
<symbol name="A4L-LOC" urn="urn:adsk.eagle:symbol:13874/1" locally_modified="yes">
<wire x1="256.54" y1="3.81" x2="256.54" y2="8.89" width="0.1016" layer="94"/>
<wire x1="256.54" y1="8.89" x2="256.54" y2="13.97" width="0.1016" layer="94"/>
<wire x1="256.54" y1="13.97" x2="256.54" y2="19.05" width="0.1016" layer="94"/>
<wire x1="256.54" y1="19.05" x2="256.54" y2="24.13" width="0.1016" layer="94"/>
<wire x1="161.29" y1="3.81" x2="161.29" y2="24.13" width="0.1016" layer="94"/>
<wire x1="161.29" y1="24.13" x2="215.265" y2="24.13" width="0.1016" layer="94"/>
<wire x1="215.265" y1="24.13" x2="256.54" y2="24.13" width="0.1016" layer="94"/>
<wire x1="246.38" y1="3.81" x2="246.38" y2="8.89" width="0.1016" layer="94"/>
<wire x1="246.38" y1="8.89" x2="256.54" y2="8.89" width="0.1016" layer="94"/>
<wire x1="246.38" y1="8.89" x2="215.265" y2="8.89" width="0.1016" layer="94"/>
<wire x1="215.265" y1="8.89" x2="215.265" y2="3.81" width="0.1016" layer="94"/>
<wire x1="215.265" y1="8.89" x2="215.265" y2="13.97" width="0.1016" layer="94"/>
<wire x1="215.265" y1="13.97" x2="256.54" y2="13.97" width="0.1016" layer="94"/>
<wire x1="215.265" y1="13.97" x2="215.265" y2="19.05" width="0.1016" layer="94"/>
<wire x1="215.265" y1="19.05" x2="256.54" y2="19.05" width="0.1016" layer="94"/>
<wire x1="215.265" y1="19.05" x2="215.265" y2="24.13" width="0.1016" layer="94"/>
<text x="217.17" y="15.24" size="2.54" layer="94">&gt;DRAWING_NAME</text>
<text x="217.17" y="10.16" size="2.286" layer="94">&gt;LAST_DATE_TIME</text>
<text x="230.505" y="5.08" size="2.54" layer="94">&gt;SHEET</text>
<text x="216.916" y="4.953" size="2.54" layer="94">Sheet:</text>
<frame x1="0" y1="0" x2="260.35" y2="179.07" columns="6" rows="4" layer="94"/>
<text x="163.83" y="20.32" size="2.286" layer="94">&gt;NOTE</text>
<text x="217.17" y="20.32" size="2.54" layer="94">&gt;SHEET_NAME</text>
</symbol>
</symbols>
<devicesets>
<deviceset name="A4L-LOC" urn="urn:adsk.eagle:component:13926/1" prefix="FRAME" uservalue="yes">
<description>&lt;b&gt;FRAME&lt;/b&gt;&lt;p&gt;
DIN A4, landscape with location and doc. field</description>
<gates>
<gate name="G$1" symbol="A4L-LOC" x="0" y="0"/>
</gates>
<devices>
<device name="">
<technologies>
<technology name=""/>
</technologies>
</device>
</devices>
</deviceset>
</devicesets>
</library>
<library name="AD8232ACPZ-R7">
<packages>
<package name="AD8232ACPZ-R7">
<rectangle x1="-0.85" y1="-0.85" x2="0.85" y2="0.85" layer="31"/>
<text x="-3" y="-3" size="1.27" layer="27" align="top-left">&gt;VALUE</text>
<text x="-3" y="3" size="1.27" layer="25">&gt;NAME</text>
<circle x="-2.975" y="1" radius="0.1" width="0.2" layer="21"/>
<circle x="-2.975" y="1" radius="0.1" width="0.2" layer="51"/>
<wire x1="2" y1="-2" x2="-2" y2="-2" width="0.127" layer="51"/>
<wire x1="2" y1="2" x2="-2" y2="2" width="0.127" layer="51"/>
<wire x1="2" y1="-2" x2="2" y2="2" width="0.127" layer="51"/>
<wire x1="-2" y1="-2" x2="-2" y2="2" width="0.127" layer="51"/>
<wire x1="2" y1="-2" x2="1.45" y2="-2" width="0.127" layer="21"/>
<wire x1="2" y1="2" x2="1.45" y2="2" width="0.127" layer="21"/>
<wire x1="-2" y1="-2" x2="-1.45" y2="-2" width="0.127" layer="21"/>
<wire x1="-2" y1="2" x2="-1.45" y2="2" width="0.127" layer="21"/>
<wire x1="2" y1="-2" x2="2" y2="-1.45" width="0.127" layer="21"/>
<wire x1="2" y1="2" x2="2" y2="1.45" width="0.127" layer="21"/>
<wire x1="-2" y1="-2" x2="-2" y2="-1.45" width="0.127" layer="21"/>
<wire x1="-2" y1="2" x2="-2" y2="1.45" width="0.127" layer="21"/>
<wire x1="-2.605" y1="-2.605" x2="2.605" y2="-2.605" width="0.05" layer="39"/>
<wire x1="-2.605" y1="2.605" x2="2.605" y2="2.605" width="0.05" layer="39"/>
<wire x1="-2.605" y1="-2.605" x2="-2.605" y2="2.605" width="0.05" layer="39"/>
<wire x1="2.605" y1="-2.605" x2="2.605" y2="2.605" width="0.05" layer="39"/>
<smd name="6" x="-1" y="-1.935" dx="0.26" dy="0.84" layer="1" roundness="25"/>
<smd name="7" x="-0.5" y="-1.935" dx="0.26" dy="0.84" layer="1" roundness="25"/>
<smd name="8" x="0" y="-1.935" dx="0.26" dy="0.84" layer="1" roundness="25"/>
<smd name="9" x="0.5" y="-1.935" dx="0.26" dy="0.84" layer="1" roundness="25"/>
<smd name="10" x="1" y="-1.935" dx="0.26" dy="0.84" layer="1" roundness="25"/>
<smd name="16" x="1" y="1.935" dx="0.26" dy="0.84" layer="1" roundness="25"/>
<smd name="17" x="0.5" y="1.935" dx="0.26" dy="0.84" layer="1" roundness="25"/>
<smd name="18" x="0" y="1.935" dx="0.26" dy="0.84" layer="1" roundness="25"/>
<smd name="19" x="-0.5" y="1.935" dx="0.26" dy="0.84" layer="1" roundness="25"/>
<smd name="20" x="-1" y="1.935" dx="0.26" dy="0.84" layer="1" roundness="25"/>
<smd name="1" x="-1.935" y="1" dx="0.84" dy="0.26" layer="1" roundness="25"/>
<smd name="2" x="-1.935" y="0.5" dx="0.84" dy="0.26" layer="1" roundness="25"/>
<smd name="3" x="-1.935" y="0" dx="0.84" dy="0.26" layer="1" roundness="25"/>
<smd name="4" x="-1.935" y="-0.5" dx="0.84" dy="0.26" layer="1" roundness="25"/>
<smd name="5" x="-1.935" y="-1" dx="0.84" dy="0.26" layer="1" roundness="25"/>
<smd name="11" x="1.935" y="-1" dx="0.84" dy="0.26" layer="1" roundness="25"/>
<smd name="12" x="1.935" y="-0.5" dx="0.84" dy="0.26" layer="1" roundness="25"/>
<smd name="13" x="1.935" y="0" dx="0.84" dy="0.26" layer="1" roundness="25"/>
<smd name="14" x="1.935" y="0.5" dx="0.84" dy="0.26" layer="1" roundness="25"/>
<smd name="15" x="1.935" y="1" dx="0.84" dy="0.26" layer="1" roundness="25"/>
<smd name="21" x="0" y="0" dx="2.7" dy="2.7" layer="1" cream="no"/>
</package>
</packages>
<symbols>
<symbol name="AD8232ACPZ-R7">
<pin name="HPDRIVE" x="-22.86" y="5.08" length="middle"/>
<pin name="IN+" x="-22.86" y="2.54" length="middle"/>
<pin name="IN-" x="-22.86" y="0" length="middle"/>
<pin name="RLDFB" x="-22.86" y="-2.54" length="middle"/>
<pin name="RLD" x="-22.86" y="-5.08" length="middle"/>
<pin name="SW" x="-5.08" y="-22.86" length="middle" rot="R90"/>
<pin name="OPAMP+" x="-2.54" y="-22.86" length="middle" rot="R90"/>
<pin name="REFOUT" x="0" y="-22.86" length="middle" rot="R90"/>
<pin name="OPAMP-" x="2.54" y="-22.86" length="middle" rot="R90"/>
<pin name="OUT" x="5.08" y="-22.86" length="middle" rot="R90"/>
<pin name="LOD-" x="22.86" y="-5.08" length="middle" rot="R180"/>
<pin name="LOD+" x="22.86" y="-2.54" length="middle" rot="R180"/>
<pin name="!SDN" x="22.86" y="0" length="middle" rot="R180"/>
<pin name="AC/!DC" x="22.86" y="2.54" length="middle" rot="R180"/>
<pin name="FR" x="22.86" y="5.08" length="middle" rot="R180"/>
<pin name="GND" x="5.08" y="22.86" length="middle" rot="R270"/>
<pin name="VS+" x="2.54" y="22.86" length="middle" rot="R270"/>
<pin name="REFIN" x="0" y="22.86" length="middle" rot="R270"/>
<pin name="IAOUT" x="-2.54" y="22.86" length="middle" rot="R270"/>
<pin name="HPSENSE" x="-5.08" y="22.86" length="middle" rot="R270"/>
<wire x1="-17.78" y1="17.78" x2="17.78" y2="17.78" width="0.254" layer="94"/>
<wire x1="17.78" y1="17.78" x2="17.78" y2="-17.78" width="0.254" layer="94"/>
<wire x1="17.78" y1="-17.78" x2="-17.78" y2="-17.78" width="0.254" layer="94"/>
<wire x1="-17.78" y1="-17.78" x2="-17.78" y2="17.78" width="0.254" layer="94"/>
<text x="10.16" y="20.32" size="1.778" layer="95">&gt;NAME</text>
<text x="10.16" y="-20.32" size="1.778" layer="96" align="top-left">&gt;VALUE</text>
</symbol>
</symbols>
<devicesets>
<deviceset name="AD8232ACPZ-R7" prefix="U">
<gates>
<gate name="G$1" symbol="AD8232ACPZ-R7" x="0" y="0"/>
</gates>
<devices>
<device name="" package="AD8232ACPZ-R7">
<connects>
<connect gate="G$1" pin="!SDN" pad="13"/>
<connect gate="G$1" pin="AC/!DC" pad="14"/>
<connect gate="G$1" pin="FR" pad="15"/>
<connect gate="G$1" pin="GND" pad="16"/>
<connect gate="G$1" pin="HPDRIVE" pad="1"/>
<connect gate="G$1" pin="HPSENSE" pad="20"/>
<connect gate="G$1" pin="IAOUT" pad="19"/>
<connect gate="G$1" pin="IN+" pad="2"/>
<connect gate="G$1" pin="IN-" pad="3"/>
<connect gate="G$1" pin="LOD+" pad="12"/>
<connect gate="G$1" pin="LOD-" pad="11"/>
<connect gate="G$1" pin="OPAMP+" pad="7"/>
<connect gate="G$1" pin="OPAMP-" pad="9"/>
<connect gate="G$1" pin="OUT" pad="10"/>
<connect gate="G$1" pin="REFIN" pad="18"/>
<connect gate="G$1" pin="REFOUT" pad="8"/>
<connect gate="G$1" pin="RLD" pad="5"/>
<connect gate="G$1" pin="RLDFB" pad="4"/>
<connect gate="G$1" pin="SW" pad="6"/>
<connect gate="G$1" pin="VS+" pad="17"/>
</connects>
<technologies>
<technology name=""/>
</technologies>
</device>
</devices>
</deviceset>
</devicesets>
</library>
<library name="ADS1219IPWR">
<packages>
<package name="SOP65P640X120-16N">
<circle x="-4.19" y="2.275" radius="0.1" width="0.2" layer="21"/>
<circle x="-4.19" y="2.275" radius="0.1" width="0.2" layer="51"/>
<wire x1="-2.2" y1="2.5" x2="2.2" y2="2.5" width="0.127" layer="51"/>
<wire x1="-2.2" y1="-2.5" x2="2.2" y2="-2.5" width="0.127" layer="51"/>
<wire x1="-1.765" y1="2.5" x2="1.765" y2="2.5" width="0.127" layer="21"/>
<wire x1="-2.2" y1="2.5" x2="-2.2" y2="-2.5" width="0.127" layer="51"/>
<wire x1="2.2" y1="2.5" x2="2.2" y2="-2.5" width="0.127" layer="51"/>
<wire x1="-3.905" y1="2.75" x2="3.905" y2="2.75" width="0.05" layer="39"/>
<wire x1="-3.905" y1="-2.75" x2="3.905" y2="-2.75" width="0.05" layer="39"/>
<wire x1="-3.905" y1="2.75" x2="-3.905" y2="-2.75" width="0.05" layer="39"/>
<wire x1="3.905" y1="2.75" x2="3.905" y2="-2.75" width="0.05" layer="39"/>
<text x="-3.5" y="-3" size="1.27" layer="27" align="top-left">&gt;VALUE</text>
<text x="-3.5" y="3" size="1.27" layer="25">&gt;NAME</text>
<wire x1="1.765" y1="-2.5" x2="-1.765" y2="-2.5" width="0.127" layer="21"/>
<smd name="1" x="-2.87" y="2.275" dx="1.57" dy="0.41" layer="1" roundness="25"/>
<smd name="2" x="-2.87" y="1.625" dx="1.57" dy="0.41" layer="1" roundness="25"/>
<smd name="3" x="-2.87" y="0.975" dx="1.57" dy="0.41" layer="1" roundness="25"/>
<smd name="4" x="-2.87" y="0.325" dx="1.57" dy="0.41" layer="1" roundness="25"/>
<smd name="5" x="-2.87" y="-0.325" dx="1.57" dy="0.41" layer="1" roundness="25"/>
<smd name="6" x="-2.87" y="-0.975" dx="1.57" dy="0.41" layer="1" roundness="25"/>
<smd name="7" x="-2.87" y="-1.625" dx="1.57" dy="0.41" layer="1" roundness="25"/>
<smd name="8" x="-2.87" y="-2.275" dx="1.57" dy="0.41" layer="1" roundness="25"/>
<smd name="9" x="2.87" y="-2.275" dx="1.57" dy="0.41" layer="1" roundness="25"/>
<smd name="10" x="2.87" y="-1.625" dx="1.57" dy="0.41" layer="1" roundness="25"/>
<smd name="11" x="2.87" y="-0.975" dx="1.57" dy="0.41" layer="1" roundness="25"/>
<smd name="12" x="2.87" y="-0.325" dx="1.57" dy="0.41" layer="1" roundness="25"/>
<smd name="13" x="2.87" y="0.325" dx="1.57" dy="0.41" layer="1" roundness="25"/>
<smd name="14" x="2.87" y="0.975" dx="1.57" dy="0.41" layer="1" roundness="25"/>
<smd name="15" x="2.87" y="1.625" dx="1.57" dy="0.41" layer="1" roundness="25"/>
<smd name="16" x="2.87" y="2.275" dx="1.57" dy="0.41" layer="1" roundness="25"/>
</package>
</packages>
<symbols>
<symbol name="ADS1219IPWR">
<wire x1="-12.7" y1="25.4" x2="12.7" y2="25.4" width="0.41" layer="94"/>
<wire x1="12.7" y1="25.4" x2="12.7" y2="-25.4" width="0.41" layer="94"/>
<wire x1="12.7" y1="-25.4" x2="-12.7" y2="-25.4" width="0.41" layer="94"/>
<wire x1="-12.7" y1="-25.4" x2="-12.7" y2="25.4" width="0.41" layer="94"/>
<text x="-12.7" y="26.4" size="2.0828" layer="95" ratio="10" rot="SR0">&gt;NAME</text>
<text x="-12.7" y="-29.4" size="2.0828" layer="96" ratio="10" rot="SR0">&gt;VALUE</text>
<pin name="!RESET" x="-17.78" y="15.24" length="middle" direction="in"/>
<pin name="A0" x="-17.78" y="12.7" length="middle" direction="in"/>
<pin name="A1" x="-17.78" y="10.16" length="middle" direction="in"/>
<pin name="AIN0" x="-17.78" y="7.62" length="middle" direction="in"/>
<pin name="AIN1" x="-17.78" y="5.08" length="middle" direction="in"/>
<pin name="AIN2" x="-17.78" y="2.54" length="middle" direction="in"/>
<pin name="AIN3" x="-17.78" y="0" length="middle" direction="in"/>
<pin name="REFN" x="-17.78" y="-2.54" length="middle" direction="in"/>
<pin name="REFP" x="-17.78" y="-5.08" length="middle" direction="in"/>
<pin name="SCL" x="-17.78" y="-7.62" length="middle" direction="in"/>
<pin name="SDA" x="-17.78" y="-12.7" length="middle"/>
<pin name="AVDD" x="17.78" y="22.86" length="middle" direction="pwr" rot="R180"/>
<pin name="DVDD" x="17.78" y="20.32" length="middle" direction="pwr" rot="R180"/>
<pin name="!DRDY" x="17.78" y="15.24" length="middle" direction="out" rot="R180"/>
<pin name="AGND" x="17.78" y="-17.78" length="middle" direction="pwr" rot="R180"/>
<pin name="DGND" x="17.78" y="-20.32" length="middle" direction="pwr" rot="R180"/>
</symbol>
</symbols>
<devicesets>
<deviceset name="ADS1219IPWR" prefix="U">
<gates>
<gate name="G$1" symbol="ADS1219IPWR" x="0" y="0"/>
</gates>
<devices>
<device name="" package="SOP65P640X120-16N">
<connects>
<connect gate="G$1" pin="!DRDY" pad="14"/>
<connect gate="G$1" pin="!RESET" pad="3"/>
<connect gate="G$1" pin="A0" pad="1"/>
<connect gate="G$1" pin="A1" pad="2"/>
<connect gate="G$1" pin="AGND" pad="5"/>
<connect gate="G$1" pin="AIN0" pad="11"/>
<connect gate="G$1" pin="AIN1" pad="10"/>
<connect gate="G$1" pin="AIN2" pad="7"/>
<connect gate="G$1" pin="AIN3" pad="6"/>
<connect gate="G$1" pin="AVDD" pad="12"/>
<connect gate="G$1" pin="DGND" pad="4"/>
<connect gate="G$1" pin="DVDD" pad="13"/>
<connect gate="G$1" pin="REFN" pad="8"/>
<connect gate="G$1" pin="REFP" pad="9"/>
<connect gate="G$1" pin="SCL" pad="16"/>
<connect gate="G$1" pin="SDA" pad="15"/>
</connects>
<technologies>
<technology name="">
<attribute name="DESCRIPTION" value=" 24-bit, 1kSPS, 4-ch general-purpose delta-sigma ADC with I2C interface and external Vref inputs "/>
<attribute name="DIGI-KEY_PART_NUMBER" value="296-50884-2-ND"/>
<attribute name="MF" value="Texas Instruments"/>
<attribute name="MP" value="ADS1219IPWR"/>
<attribute name="PACKAGE" value="TSSOP-16 Texas Instruments"/>
<attribute name="PURCHASE-URL" value="https://pricing.snapeda.com/search/part/ADS1219IPWR/?ref=eda"/>
</technology>
</technologies>
</device>
</devices>
</deviceset>
</devicesets>
</library>
<library name="0-Standard-Passives">
<packages>
<package name="R0402" urn="urn:adsk.eagle:footprint:23043/3">
<description>&lt;b&gt;Chip RESISTOR 0402 EIA (1005 Metric)&lt;/b&gt;</description>
<wire x1="-0.245" y1="0.224" x2="0.245" y2="0.224" width="0.1524" layer="51"/>
<wire x1="0.245" y1="-0.224" x2="-0.245" y2="-0.224" width="0.1524" layer="51"/>
<wire x1="-1" y1="0.483" x2="1" y2="0.483" width="0.0508" layer="39"/>
<wire x1="1" y1="0.483" x2="1" y2="-0.483" width="0.0508" layer="39"/>
<wire x1="1" y1="-0.483" x2="-1" y2="-0.483" width="0.0508" layer="39"/>
<wire x1="-1" y1="-0.483" x2="-1" y2="0.483" width="0.0508" layer="39"/>
<smd name="1" x="-0.5" y="0" dx="0.6" dy="0.7" layer="1"/>
<smd name="2" x="0.5" y="0" dx="0.6" dy="0.7" layer="1"/>
<text x="-0.635" y="0.635" size="1.27" layer="25">&gt;NAME</text>
<text x="-0.635" y="-1.905" size="1.27" layer="27">&gt;VALUE</text>
<rectangle x1="-0.554" y1="-0.3048" x2="-0.254" y2="0.2951" layer="51"/>
<rectangle x1="0.2588" y1="-0.3048" x2="0.5588" y2="0.2951" layer="51"/>
<rectangle x1="-0.1999" y1="-0.35" x2="0.1999" y2="0.35" layer="35"/>
</package>
<package name="C0402" urn="urn:adsk.eagle:footprint:23121/1" locally_modified="yes">
<description>&lt;b&gt;CAPACITOR&lt;/b&gt;</description>
<wire x1="-0.245" y1="0.224" x2="0.245" y2="0.224" width="0.1524" layer="51"/>
<wire x1="0.245" y1="-0.224" x2="-0.245" y2="-0.224" width="0.1524" layer="51"/>
<wire x1="-1" y1="0.483" x2="1" y2="0.483" width="0.0508" layer="39"/>
<wire x1="1" y1="0.483" x2="1" y2="-0.483" width="0.0508" layer="39"/>
<wire x1="1" y1="-0.483" x2="-1" y2="-0.483" width="0.0508" layer="39"/>
<wire x1="-1" y1="-0.483" x2="-1" y2="0.483" width="0.0508" layer="39"/>
<smd name="1" x="-0.5" y="0" dx="0.6" dy="0.7" layer="1"/>
<smd name="2" x="0.5" y="0" dx="0.6" dy="0.7" layer="1"/>
<text x="-0.635" y="0.635" size="1.27" layer="25">&gt;NAME</text>
<text x="-0.635" y="-1.905" size="1.27" layer="27">&gt;VALUE</text>
<rectangle x1="-0.554" y1="-0.3048" x2="-0.254" y2="0.2951" layer="51"/>
<rectangle x1="0.2588" y1="-0.3048" x2="0.5588" y2="0.2951" layer="51"/>
<rectangle x1="-0.1999" y1="-0.3" x2="0.1999" y2="0.3" layer="35"/>
</package>
</packages>
<packages3d>
<package3d name="R0402" urn="urn:adsk.eagle:package:23547/3" type="model">
<description>Chip RESISTOR 0402 EIA (1005 Metric)</description>
<packageinstances>
<packageinstance name="R0402"/>
</packageinstances>
</package3d>
</packages3d>
<symbols>
<symbol name="R-STANDARD">
<wire x1="-2.54" y1="0" x2="-2.159" y2="1.016" width="0.2032" layer="94"/>
<wire x1="-2.159" y1="1.016" x2="-1.524" y2="-1.016" width="0.2032" layer="94"/>
<wire x1="-1.524" y1="-1.016" x2="-0.889" y2="1.016" width="0.2032" layer="94"/>
<wire x1="-0.889" y1="1.016" x2="-0.254" y2="-1.016" width="0.2032" layer="94"/>
<wire x1="-0.254" y1="-1.016" x2="0.381" y2="1.016" width="0.2032" layer="94"/>
<wire x1="0.381" y1="1.016" x2="1.016" y2="-1.016" width="0.2032" layer="94"/>
<wire x1="1.016" y1="-1.016" x2="1.651" y2="1.016" width="0.2032" layer="94"/>
<wire x1="1.651" y1="1.016" x2="2.286" y2="-1.016" width="0.2032" layer="94"/>
<wire x1="2.286" y1="-1.016" x2="2.54" y2="0" width="0.2032" layer="94"/>
<text x="-3.81" y="1.4986" size="1.778" layer="95">&gt;NAME</text>
<text x="-3.81" y="-3.302" size="1.778" layer="96">&gt;VALUE</text>
<pin name="2" x="5.08" y="0" visible="off" length="short" direction="pas" swaplevel="1" rot="R180"/>
<pin name="1" x="-5.08" y="0" visible="off" length="short" direction="pas" swaplevel="1"/>
</symbol>
<symbol name="C-STANDARD">
<wire x1="0" y1="0" x2="0" y2="-0.508" width="0.1524" layer="94"/>
<wire x1="0" y1="-2.54" x2="0" y2="-2.032" width="0.1524" layer="94"/>
<text x="1.524" y="0.381" size="1.778" layer="95">&gt;NAME</text>
<text x="1.524" y="-4.699" size="1.778" layer="96">&gt;VALUE</text>
<rectangle x1="-2.032" y1="-2.032" x2="2.032" y2="-1.524" layer="94"/>
<rectangle x1="-2.032" y1="-1.016" x2="2.032" y2="-0.508" layer="94"/>
<pin name="1" x="0" y="2.54" visible="off" length="short" direction="pas" swaplevel="1" rot="R270"/>
<pin name="2" x="0" y="-5.08" visible="off" length="short" direction="pas" swaplevel="1" rot="R90"/>
</symbol>
</symbols>
<devicesets>
<deviceset name="RES,SMD,10MOHM,1%,1/10W,0402" prefix="R">
<gates>
<gate name="G$1" symbol="R-STANDARD" x="0" y="0"/>
</gates>
<devices>
<device name="" package="R0402">
<connects>
<connect gate="G$1" pin="1" pad="1"/>
<connect gate="G$1" pin="2" pad="2"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:23547/3"/>
</package3dinstances>
<technologies>
<technology name="">
<attribute name="VALUE" value="10Mohm"/>
</technology>
</technologies>
</device>
</devices>
</deviceset>
<deviceset name="RES,SMD,182KOHM,1%,1/10W,0402" prefix="R">
<gates>
<gate name="G$1" symbol="R-STANDARD" x="0" y="0"/>
</gates>
<devices>
<device name="" package="R0402">
<connects>
<connect gate="G$1" pin="1" pad="1"/>
<connect gate="G$1" pin="2" pad="2"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:23547/3"/>
</package3dinstances>
<technologies>
<technology name="">
<attribute name="VALUE" value="182kohm"/>
</technology>
</technologies>
</device>
</devices>
</deviceset>
<deviceset name="RES,SMD,100KOHM,10%,1/10W,0402" prefix="R">
<gates>
<gate name="G$1" symbol="R-STANDARD" x="0" y="0"/>
</gates>
<devices>
<device name="" package="R0402">
<connects>
<connect gate="G$1" pin="1" pad="1"/>
<connect gate="G$1" pin="2" pad="2"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:23547/3"/>
</package3dinstances>
<technologies>
<technology name="">
<attribute name="VALUE" value="100kohm"/>
</technology>
</technologies>
</device>
</devices>
</deviceset>
<deviceset name="RES,SMD,1MOHM,1%,1/10W,0402" prefix="R">
<gates>
<gate name="G$1" symbol="R-STANDARD" x="0" y="0"/>
</gates>
<devices>
<device name="" package="R0402">
<connects>
<connect gate="G$1" pin="1" pad="1"/>
<connect gate="G$1" pin="2" pad="2"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:23547/3"/>
</package3dinstances>
<technologies>
<technology name="">
<attribute name="VALUE" value="1Mohm"/>
</technology>
</technologies>
</device>
</devices>
</deviceset>
<deviceset name="RES,SMD,649KOHM,1%,1/10W,0402" prefix="R">
<gates>
<gate name="G$1" symbol="R-STANDARD" x="0" y="0"/>
</gates>
<devices>
<device name="" package="R0402">
<connects>
<connect gate="G$1" pin="1" pad="1"/>
<connect gate="G$1" pin="2" pad="2"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:23547/3"/>
</package3dinstances>
<technologies>
<technology name="">
<attribute name="VALUE" value="649kohm"/>
</technology>
</technologies>
</device>
</devices>
</deviceset>
<deviceset name="CAP,CER,1UF,10V,10%,X5R,0402" prefix="C">
<gates>
<gate name="G$1" symbol="C-STANDARD" x="0" y="0"/>
</gates>
<devices>
<device name="" package="C0402">
<connects>
<connect gate="G$1" pin="1" pad="1"/>
<connect gate="G$1" pin="2" pad="2"/>
</connects>
<technologies>
<technology name="">
<attribute name="VALUE" value="1uF"/>
</technology>
</technologies>
</device>
</devices>
</deviceset>
<deviceset name="CAP,CER,6.2NF,25V,10%,X7R,0402" prefix="C">
<gates>
<gate name="G$1" symbol="C-STANDARD" x="0" y="0"/>
</gates>
<devices>
<device name="" package="C0402">
<connects>
<connect gate="G$1" pin="1" pad="1"/>
<connect gate="G$1" pin="2" pad="2"/>
</connects>
<technologies>
<technology name="">
<attribute name="VALUE" value="6.2nF"/>
</technology>
</technologies>
</device>
</devices>
</deviceset>
<deviceset name="CAP,CER,1000PF,2KV,10%,X7R,0402" prefix="C">
<gates>
<gate name="A" symbol="C-STANDARD" x="0" y="0"/>
</gates>
<devices>
<device name="" package="C0402">
<connects>
<connect gate="A" pin="1" pad="1"/>
<connect gate="A" pin="2" pad="2"/>
</connects>
<technologies>
<technology name="">
<attribute name="VALUE" value="1000pF"/>
</technology>
</technologies>
</device>
</devices>
</deviceset>
<deviceset name="CAP,CER,0.1UF,16V,10%,X5R,0402" prefix="C">
<gates>
<gate name="G$1" symbol="C-STANDARD" x="0" y="0"/>
</gates>
<devices>
<device name="" package="C0402">
<connects>
<connect gate="G$1" pin="1" pad="1"/>
<connect gate="G$1" pin="2" pad="2"/>
</connects>
<technologies>
<technology name="">
<attribute name="VALUE" value="0.1uF"/>
</technology>
</technologies>
</device>
</devices>
</deviceset>
<deviceset name="RES,SMD,0OHM,5%,1/16W,0402" prefix="R">
<gates>
<gate name="G$1" symbol="R-STANDARD" x="0" y="0"/>
</gates>
<devices>
<device name="" package="R0402">
<connects>
<connect gate="G$1" pin="1" pad="1"/>
<connect gate="G$1" pin="2" pad="2"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:23547/3"/>
</package3dinstances>
<technologies>
<technology name="">
<attribute name="VALUE" value="0ohm"/>
</technology>
</technologies>
</device>
</devices>
</deviceset>
<deviceset name="RES,SMD,10KOHM,1%,1/16W,0402" prefix="R">
<gates>
<gate name="G$1" symbol="R-STANDARD" x="0" y="0"/>
</gates>
<devices>
<device name="" package="R0402">
<connects>
<connect gate="G$1" pin="1" pad="1"/>
<connect gate="G$1" pin="2" pad="2"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:23547/3"/>
</package3dinstances>
<technologies>
<technology name="">
<attribute name="VALUE" value="10kohm"/>
</technology>
</technologies>
</device>
</devices>
</deviceset>
<deviceset name="RES,SMD,100OHM,5%,1/10W,0402" prefix="R">
<gates>
<gate name="G$1" symbol="R-STANDARD" x="0" y="0"/>
</gates>
<devices>
<device name="" package="R0402">
<connects>
<connect gate="G$1" pin="1" pad="1"/>
<connect gate="G$1" pin="2" pad="2"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:23547/3"/>
</package3dinstances>
<technologies>
<technology name="">
<attribute name="VALUE" value="100ohm"/>
</technology>
</technologies>
</device>
</devices>
</deviceset>
</devicesets>
</library>
<library name="0-Custom-Markers">
<packages>
</packages>
<symbols>
<symbol name="GND">
<wire x1="-1.27" y1="0" x2="1.27" y2="0" width="0.254" layer="94"/>
<wire x1="1.27" y1="0" x2="0" y2="-1.27" width="0.254" layer="94"/>
<wire x1="0" y1="-1.27" x2="-1.27" y2="0" width="0.254" layer="94"/>
<pin name="GND" x="0" y="2.54" visible="off" length="short" direction="sup" rot="R270"/>
</symbol>
<symbol name="ON-PAGE">
<wire x1="-3.048" y1="0" x2="-4.318" y2="-1.27" width="0.1524" layer="94"/>
<wire x1="-3.048" y1="0" x2="-4.318" y2="1.27" width="0.1524" layer="94"/>
<wire x1="-2.54" y1="0" x2="-3.81" y2="-1.27" width="0.1524" layer="94"/>
<wire x1="-2.54" y1="0" x2="-3.81" y2="1.27" width="0.1524" layer="94"/>
<pin name="IN" x="0" y="0" visible="off" length="short" direction="in" rot="R180"/>
</symbol>
<symbol name="OFF-PAGE">
<wire x1="3.81" y1="0" x2="2.54" y2="1.27" width="0.1524" layer="94"/>
<wire x1="3.81" y1="0" x2="2.54" y2="-1.27" width="0.1524" layer="94"/>
<wire x1="4.318" y1="0" x2="3.048" y2="1.27" width="0.1524" layer="94"/>
<wire x1="4.318" y1="0" x2="3.048" y2="-1.27" width="0.1524" layer="94"/>
<pin name="OUT" x="0" y="0" visible="off" length="short" direction="out"/>
<wire x1="2.54" y1="0" x2="3.81" y2="0" width="0.1524" layer="94"/>
</symbol>
<symbol name="V+">
<wire x1="1.27" y1="0.635" x2="0" y2="2.54" width="0.254" layer="94"/>
<wire x1="0" y1="2.54" x2="-1.27" y2="0.635" width="0.254" layer="94"/>
<pin name="V+" x="0" y="0" visible="off" length="short" direction="pwr" rot="R90"/>
</symbol>
</symbols>
<devicesets>
<deviceset name="GND">
<gates>
<gate name="G$1" symbol="GND" x="0" y="-2.54"/>
</gates>
<devices>
<device name="">
<technologies>
<technology name="">
<attribute name="_EXTERNAL_" value=""/>
</technology>
</technologies>
</device>
</devices>
</deviceset>
<deviceset name="ON-PAGE">
<gates>
<gate name="G$1" symbol="ON-PAGE" x="0" y="0"/>
</gates>
<devices>
<device name="">
<technologies>
<technology name="">
<attribute name="_EXTERNAL_" value=""/>
</technology>
</technologies>
</device>
</devices>
</deviceset>
<deviceset name="OFF-PAGE">
<gates>
<gate name="G$1" symbol="OFF-PAGE" x="0" y="0"/>
</gates>
<devices>
<device name="">
<technologies>
<technology name="">
<attribute name="_EXTERNAL_" value=""/>
</technology>
</technologies>
</device>
</devices>
</deviceset>
<deviceset name="V-RAIL">
<gates>
<gate name="G$1" symbol="V+" x="0" y="0"/>
</gates>
<devices>
<device name="">
<technologies>
<technology name="">
<attribute name="_EXTERNAL_" value=""/>
</technology>
</technologies>
</device>
</devices>
</deviceset>
</devicesets>
</library>
<library name="testpad" urn="urn:adsk.eagle:library:385">
<description>&lt;b&gt;Test Pins/Pads&lt;/b&gt;&lt;p&gt;
Cream on SMD OFF.&lt;br&gt;
new: Attribute TP_SIGNAL_NAME&lt;br&gt;
&lt;author&gt;Created by librarian@cadsoft.de&lt;/author&gt;</description>
<packages>
<package name="B1,27" urn="urn:adsk.eagle:footprint:27900/1" library_version="3">
<description>&lt;b&gt;TEST PAD&lt;/b&gt;</description>
<wire x1="-0.635" y1="0" x2="0.635" y2="0" width="0.0024" layer="37"/>
<wire x1="0" y1="0.635" x2="0" y2="-0.635" width="0.0024" layer="37"/>
<smd name="TP" x="0" y="0" dx="1.27" dy="1.27" layer="1" roundness="100" cream="no"/>
<text x="-0.635" y="1.016" size="1.27" layer="25" ratio="10">&gt;NAME</text>
<text x="-0.635" y="-0.762" size="0.0254" layer="27">&gt;VALUE</text>
<text x="-0.635" y="-1.905" size="1" layer="37">&gt;TP_SIGNAL_NAME</text>
</package>
<package name="B2,54" urn="urn:adsk.eagle:footprint:27901/1" library_version="3">
<description>&lt;b&gt;TEST PAD&lt;/b&gt;</description>
<wire x1="-0.635" y1="0" x2="0.635" y2="0" width="0.0024" layer="37"/>
<wire x1="0" y1="-0.635" x2="0" y2="0.635" width="0.0024" layer="37"/>
<circle x="0" y="0" radius="0.635" width="0.254" layer="37"/>
<smd name="TP" x="0" y="0" dx="2.54" dy="2.54" layer="1" roundness="100" cream="no"/>
<text x="-1.27" y="1.651" size="1.27" layer="25" ratio="10">&gt;NAME</text>
<text x="-1.27" y="-1.397" size="0.0254" layer="27">&gt;VALUE</text>
<text x="-1.27" y="-3.175" size="1" layer="37">&gt;TP_SIGNAL_NAME</text>
</package>
<package name="P1-13" urn="urn:adsk.eagle:footprint:27902/1" library_version="3">
<description>&lt;b&gt;TEST PAD&lt;/b&gt;</description>
<circle x="0" y="0" radius="0.762" width="0.1524" layer="51"/>
<pad name="TP" x="0" y="0" drill="1.3208" diameter="2.159" shape="octagon"/>
<text x="-1.016" y="1.27" size="1.27" layer="25" ratio="10">&gt;NAME</text>
<text x="0" y="0" size="0.0254" layer="27">&gt;VALUE</text>
<text x="-1.27" y="-2.54" size="1" layer="37">&gt;TP_SIGNAL_NAME</text>
<rectangle x1="-0.3302" y1="-0.3302" x2="0.3302" y2="0.3302" layer="51"/>
</package>
<package name="P1-13Y" urn="urn:adsk.eagle:footprint:27903/1" library_version="3">
<description>&lt;b&gt;TEST PAD&lt;/b&gt;</description>
<circle x="0" y="0" radius="0.762" width="0.1524" layer="51"/>
<pad name="TP" x="0" y="0" drill="1.3208" diameter="1.905" shape="long" rot="R90"/>
<text x="-0.889" y="2.159" size="1.27" layer="25" ratio="10">&gt;NAME</text>
<text x="0" y="0" size="0.0254" layer="27">&gt;VALUE</text>
<text x="-1.27" y="-3.81" size="1" layer="37">&gt;TP_SIGNAL_NAME</text>
<rectangle x1="-0.3302" y1="-0.3302" x2="0.3302" y2="0.3302" layer="51"/>
</package>
<package name="P1-17" urn="urn:adsk.eagle:footprint:27904/1" library_version="3">
<description>&lt;b&gt;TEST PAD&lt;/b&gt;</description>
<circle x="0" y="0" radius="0.8128" width="0.1524" layer="51"/>
<pad name="TP" x="0" y="0" drill="1.7018" diameter="2.54" shape="octagon"/>
<text x="-1.143" y="1.397" size="1.27" layer="25" ratio="10">&gt;NAME</text>
<text x="0" y="0" size="0.0254" layer="27">&gt;VALUE</text>
<text x="-1.27" y="-3.175" size="1" layer="37">&gt;TP_SIGNAL_NAME</text>
<rectangle x1="-0.3302" y1="-0.3302" x2="0.3302" y2="0.3302" layer="51"/>
</package>
<package name="P1-17Y" urn="urn:adsk.eagle:footprint:27905/1" library_version="3">
<description>&lt;b&gt;TEST PAD&lt;/b&gt;</description>
<circle x="0" y="0" radius="0.8128" width="0.1524" layer="51"/>
<pad name="TP" x="0" y="0" drill="1.7018" diameter="2.1208" shape="long" rot="R90"/>
<text x="-1.143" y="2.286" size="1.27" layer="25" ratio="10">&gt;NAME</text>
<text x="0" y="0" size="0.0254" layer="27">&gt;VALUE</text>
<text x="-1.27" y="-3.81" size="1" layer="37">&gt;TP_SIGNAL_NAME</text>
<rectangle x1="-0.3302" y1="-0.3302" x2="0.3302" y2="0.3302" layer="51"/>
</package>
<package name="P1-20" urn="urn:adsk.eagle:footprint:27906/1" library_version="3">
<description>&lt;b&gt;TEST PAD&lt;/b&gt;</description>
<circle x="0" y="0" radius="1.016" width="0.1524" layer="51"/>
<pad name="TP" x="0" y="0" drill="2.0066" diameter="3.1496" shape="octagon"/>
<text x="-1.524" y="1.778" size="1.27" layer="25" ratio="10">&gt;NAME</text>
<text x="0" y="0" size="0.0254" layer="27">&gt;VALUE</text>
<text x="-1.27" y="-3.175" size="1" layer="37">&gt;TP_SIGNAL_NAME</text>
<rectangle x1="-0.3302" y1="-0.3302" x2="0.3302" y2="0.3302" layer="51"/>
</package>
<package name="P1-20Y" urn="urn:adsk.eagle:footprint:27907/1" library_version="3">
<description>&lt;b&gt;TEST PAD&lt;/b&gt;</description>
<circle x="0" y="0" radius="1.016" width="0.1524" layer="51"/>
<pad name="TP" x="0" y="0" drill="2.0066" diameter="2.54" shape="long" rot="R90"/>
<text x="-1.27" y="2.794" size="1.27" layer="25" ratio="10">&gt;NAME</text>
<text x="0" y="0" size="0.0254" layer="27">&gt;VALUE</text>
<text x="-1.27" y="-4.445" size="1" layer="37">&gt;TP_SIGNAL_NAME</text>
<rectangle x1="-0.3302" y1="-0.3302" x2="0.3302" y2="0.3302" layer="51"/>
</package>
<package name="TP06R" urn="urn:adsk.eagle:footprint:27908/1" library_version="3">
<description>&lt;b&gt;TEST PAD&lt;/b&gt;</description>
<smd name="TP" x="0" y="0" dx="0.6" dy="0.6" layer="1" roundness="100" cream="no"/>
<text x="-0.3" y="0.4001" size="1.27" layer="25">&gt;NAME</text>
<text x="-0.254" y="-0.381" size="0.0254" layer="27">&gt;VALUE</text>
<text x="0" y="-1.905" size="1" layer="37">&gt;TP_SIGNAL_NAME</text>
</package>
<package name="TP06SQ" urn="urn:adsk.eagle:footprint:27909/1" library_version="3">
<description>&lt;b&gt;TEST PAD&lt;/b&gt;</description>
<smd name="TP" x="0" y="0" dx="0.5996" dy="0.5996" layer="1" cream="no"/>
<text x="-0.3" y="0.4001" size="1.27" layer="25">&gt;NAME</text>
<text x="-0.254" y="-0.381" size="0.0254" layer="27">&gt;VALUE</text>
<text x="0" y="-1.905" size="1" layer="37">&gt;TP_SIGNAL_NAME</text>
</package>
<package name="TP07R" urn="urn:adsk.eagle:footprint:27910/1" library_version="3">
<description>&lt;b&gt;TEST PAD&lt;/b&gt;</description>
<smd name="TP" x="0" y="0" dx="0.7" dy="0.7" layer="1" roundness="100" cream="no"/>
<text x="-0.3" y="0.4001" size="1.27" layer="25">&gt;NAME</text>
<text x="-0.254" y="-0.508" size="0.0254" layer="27">&gt;VALUE</text>
<text x="0" y="-1.905" size="1" layer="37">&gt;TP_SIGNAL_NAME</text>
</package>
<package name="TP07SQ" urn="urn:adsk.eagle:footprint:27911/1" library_version="3">
<description>&lt;b&gt;TEST PAD&lt;/b&gt;</description>
<smd name="TP" x="0" y="0" dx="0.7" dy="0.7" layer="1" cream="no"/>
<text x="-0.3" y="0.4001" size="1.27" layer="25">&gt;NAME</text>
<text x="-0.381" y="-0.381" size="0.0254" layer="27">&gt;VALUE</text>
<text x="0" y="-1.905" size="1" layer="37">&gt;TP_SIGNAL_NAME</text>
</package>
<package name="TP08R" urn="urn:adsk.eagle:footprint:27912/1" library_version="3">
<description>&lt;b&gt;TEST PAD&lt;/b&gt;</description>
<smd name="TP" x="0" y="0" dx="0.8" dy="0.8" layer="1" roundness="100" cream="no"/>
<text x="-0.3" y="0.4001" size="1.27" layer="25">&gt;NAME</text>
<text x="-0.381" y="-0.381" size="0.0254" layer="27">&gt;VALUE</text>
<text x="0" y="-1.905" size="1" layer="37">&gt;TP_SIGNAL_NAME</text>
</package>
<package name="TP08SQ" urn="urn:adsk.eagle:footprint:27913/1" library_version="3">
<description>&lt;b&gt;TEST PAD&lt;/b&gt;</description>
<smd name="TP" x="0" y="0" dx="0.8" dy="0.8" layer="1" cream="no"/>
<text x="-0.3" y="0.4001" size="1.27" layer="25">&gt;NAME</text>
<text x="-0.381" y="-0.508" size="0.0254" layer="27">&gt;VALUE</text>
<text x="0" y="-1.905" size="1" layer="37">&gt;TP_SIGNAL_NAME</text>
</package>
<package name="TP09R" urn="urn:adsk.eagle:footprint:27914/1" library_version="3">
<description>&lt;b&gt;TEST PAD&lt;/b&gt;</description>
<smd name="TP" x="0" y="0" dx="0.9" dy="0.9" layer="1" roundness="100" cream="no"/>
<text x="-0.4501" y="0.5001" size="1.27" layer="25">&gt;NAME</text>
<text x="-0.381" y="-0.508" size="0.0254" layer="27">&gt;VALUE</text>
<text x="0" y="-1.905" size="1" layer="37">&gt;TP_SIGNAL_NAME</text>
</package>
<package name="TP09SQ" urn="urn:adsk.eagle:footprint:27915/1" library_version="3">
<description>&lt;b&gt;TEST PAD&lt;/b&gt;</description>
<smd name="TP" x="0" y="0" dx="0.8998" dy="0.8998" layer="1" cream="no"/>
<text x="-0.4501" y="0.5001" size="1.27" layer="25">&gt;NAME</text>
<text x="-0.381" y="-0.508" size="0.0254" layer="27">&gt;VALUE</text>
<text x="0" y="-1.905" size="1" layer="37">&gt;TP_SIGNAL_NAME</text>
</package>
<package name="TP10R" urn="urn:adsk.eagle:footprint:27916/1" library_version="3">
<description>&lt;b&gt;TEST PAD&lt;/b&gt;</description>
<smd name="TP" x="0" y="0" dx="1" dy="1" layer="1" roundness="100" cream="no"/>
<text x="-0.5001" y="0.5499" size="1.27" layer="25">&gt;NAME</text>
<text x="-0.381" y="-0.508" size="0.0254" layer="27">&gt;VALUE</text>
<text x="0" y="-1.905" size="1" layer="37">&gt;TP_SIGNAL_NAME</text>
</package>
<package name="TP10SQ" urn="urn:adsk.eagle:footprint:27917/1" library_version="3">
<description>&lt;b&gt;TEST PAD&lt;/b&gt;</description>
<smd name="TP" x="0" y="0" dx="1" dy="1" layer="1" cream="no"/>
<text x="-0.5001" y="0.5499" size="1.27" layer="25">&gt;NAME</text>
<text x="-0.508" y="-0.635" size="0.0254" layer="27">&gt;VALUE</text>
<text x="0" y="-1.905" size="1" layer="37">&gt;TP_SIGNAL_NAME</text>
</package>
<package name="TP11R" urn="urn:adsk.eagle:footprint:27918/1" library_version="3">
<description>&lt;b&gt;TEST PAD&lt;/b&gt;</description>
<smd name="TP" x="0" y="0" dx="1.1" dy="1.1" layer="1" roundness="100" cream="no"/>
<text x="-0.5499" y="0.5999" size="1.27" layer="25">&gt;NAME</text>
<text x="-0.508" y="-0.508" size="0.0254" layer="27">&gt;VALUE</text>
<text x="0" y="-1.905" size="1" layer="37">&gt;TP_SIGNAL_NAME</text>
</package>
<package name="TP11SQ" urn="urn:adsk.eagle:footprint:27919/1" library_version="3">
<description>&lt;b&gt;TEST PAD&lt;/b&gt;</description>
<smd name="TP" x="0" y="0" dx="1.1" dy="1.1" layer="1" cream="no"/>
<text x="-0.5499" y="0.5999" size="1.27" layer="25">&gt;NAME</text>
<text x="-0.508" y="-0.635" size="0.0254" layer="27">&gt;VALUE</text>
<text x="0" y="-2.54" size="1" layer="37">&gt;TP_SIGNAL_NAME</text>
</package>
<package name="TP12SQ" urn="urn:adsk.eagle:footprint:27920/1" library_version="3">
<description>&lt;b&gt;TEST PAD&lt;/b&gt;</description>
<smd name="TP" x="0" y="0" dx="1.1998" dy="1.1998" layer="1" cream="no"/>
<text x="-0.5999" y="0.65" size="1.27" layer="25">&gt;NAME</text>
<text x="-0.508" y="-0.635" size="0.0254" layer="27">&gt;VALUE</text>
<text x="0" y="-2.54" size="1" layer="37">&gt;TP_SIGNAL_NAME</text>
</package>
<package name="TP12R" urn="urn:adsk.eagle:footprint:27921/1" library_version="3">
<description>&lt;b&gt;TEST PAD&lt;/b&gt;</description>
<smd name="TP" x="0" y="0" dx="1.2" dy="1.2" layer="1" roundness="100" cream="no"/>
<text x="-0.5999" y="0.65" size="1.27" layer="25">&gt;NAME</text>
<text x="-0.508" y="-0.635" size="0.0254" layer="27">&gt;VALUE</text>
<text x="0" y="-2.54" size="1" layer="37">&gt;TP_SIGNAL_NAME</text>
</package>
<package name="TP13R" urn="urn:adsk.eagle:footprint:27922/1" library_version="3">
<description>&lt;b&gt;TEST PAD&lt;/b&gt;</description>
<smd name="TP" x="0" y="0" dx="1.3" dy="1.3" layer="1" roundness="100" cream="no"/>
<text x="-0.65" y="0.7" size="1.27" layer="25">&gt;NAME</text>
<text x="-0.508" y="-0.635" size="0.0254" layer="27">&gt;VALUE</text>
<text x="0" y="-2.54" size="1" layer="37">&gt;TP_SIGNAL_NAME</text>
</package>
<package name="TP14R" urn="urn:adsk.eagle:footprint:27923/1" library_version="3">
<description>&lt;b&gt;TEST PAD&lt;/b&gt;</description>
<smd name="TP" x="0" y="0" dx="1.4" dy="1.4" layer="1" roundness="100" cream="no"/>
<text x="-0.7" y="0.7501" size="1.27" layer="25">&gt;NAME</text>
<text x="-0.508" y="-0.762" size="0.0254" layer="27">&gt;VALUE</text>
<text x="0" y="-2.54" size="1" layer="37">&gt;TP_SIGNAL_NAME</text>
</package>
<package name="TP15R" urn="urn:adsk.eagle:footprint:27924/1" library_version="3">
<description>&lt;b&gt;TEST PAD&lt;/b&gt;</description>
<smd name="TP" x="0" y="0" dx="1.5" dy="1.5" layer="1" roundness="100" cream="no"/>
<text x="-0.7501" y="0.8001" size="1.27" layer="25">&gt;NAME</text>
<text x="-0.635" y="-0.762" size="0.0254" layer="27">&gt;VALUE</text>
<text x="0" y="-2.54" size="1" layer="37">&gt;TP_SIGNAL_NAME</text>
</package>
<package name="TP16R" urn="urn:adsk.eagle:footprint:27925/1" library_version="3">
<description>&lt;b&gt;TEST PAD&lt;/b&gt;</description>
<smd name="TP" x="0" y="0" dx="1.6" dy="1.6" layer="1" roundness="100" cream="no"/>
<text x="-0.8001" y="0.8499" size="1.27" layer="25">&gt;NAME</text>
<text x="-0.635" y="-0.762" size="0.0254" layer="27">&gt;VALUE</text>
<text x="0" y="-2.54" size="1" layer="37">&gt;TP_SIGNAL_NAME</text>
</package>
<package name="TP17R" urn="urn:adsk.eagle:footprint:27926/1" library_version="3">
<description>&lt;b&gt;TEST PAD&lt;/b&gt;</description>
<smd name="TP" x="0" y="0" dx="1.7" dy="1.7" layer="1" roundness="100" cream="no"/>
<text x="-0.8499" y="0.8999" size="1.27" layer="25">&gt;NAME</text>
<text x="-0.635" y="-0.889" size="0.0254" layer="27">&gt;VALUE</text>
<text x="0" y="-2.54" size="1" layer="37">&gt;TP_SIGNAL_NAME</text>
</package>
<package name="TP18R" urn="urn:adsk.eagle:footprint:27927/1" library_version="3">
<description>&lt;b&gt;TEST PAD&lt;/b&gt;</description>
<smd name="TP" x="0" y="0" dx="1.8" dy="1.8" layer="1" roundness="100" cream="no"/>
<text x="-0.8999" y="0.95" size="1.27" layer="25">&gt;NAME</text>
<text x="-0.762" y="-0.889" size="0.0254" layer="27">&gt;VALUE</text>
<text x="0" y="-2.54" size="1" layer="37">&gt;TP_SIGNAL_NAME</text>
</package>
<package name="TP19R" urn="urn:adsk.eagle:footprint:27928/1" library_version="3">
<description>&lt;b&gt;TEST PAD&lt;/b&gt;</description>
<smd name="TP" x="0" y="0" dx="1.9" dy="1.9" layer="1" roundness="100" cream="no"/>
<text x="-0.95" y="1" size="1.27" layer="25">&gt;NAME</text>
<text x="-0.762" y="-0.889" size="0.0254" layer="27">&gt;VALUE</text>
<text x="0" y="-2.54" size="1" layer="37">&gt;TP_SIGNAL_NAME</text>
</package>
<package name="TP20R" urn="urn:adsk.eagle:footprint:27929/1" library_version="3">
<description>&lt;b&gt;TEST PAD&lt;/b&gt;</description>
<smd name="TP" x="0" y="0" dx="2" dy="2" layer="1" roundness="100" cream="no"/>
<text x="-1" y="1.05" size="1.27" layer="25">&gt;NAME</text>
<text x="-0.762" y="-1.016" size="0.0254" layer="27">&gt;VALUE</text>
<text x="0" y="-2.54" size="1" layer="37">&gt;TP_SIGNAL_NAME</text>
</package>
<package name="TP13SQ" urn="urn:adsk.eagle:footprint:27930/1" library_version="3">
<description>&lt;b&gt;TEST PAD&lt;/b&gt;</description>
<smd name="TP" x="0" y="0" dx="1.3" dy="1.3" layer="1" cream="no"/>
<text x="-0.65" y="0.7" size="1.27" layer="25">&gt;NAME</text>
<text x="-0.635" y="-0.762" size="0.0254" layer="27">&gt;VALUE</text>
<text x="0" y="-2.54" size="1" layer="37">&gt;TP_SIGNAL_NAME</text>
</package>
<package name="TP14SQ" urn="urn:adsk.eagle:footprint:27931/1" library_version="3">
<description>&lt;b&gt;TEST PAD&lt;/b&gt;</description>
<smd name="TP" x="0" y="0" dx="1.4" dy="1.4" layer="1" cream="no"/>
<text x="-0.7" y="0.7501" size="1.27" layer="25">&gt;NAME</text>
<text x="-0.635" y="-0.762" size="0.0254" layer="27">&gt;VALUE</text>
<text x="0" y="-2.54" size="1" layer="37">&gt;TP_SIGNAL_NAME</text>
</package>
<package name="TP15SQ" urn="urn:adsk.eagle:footprint:27932/1" library_version="3">
<description>&lt;b&gt;TEST PAD&lt;/b&gt;</description>
<smd name="TP" x="0" y="0" dx="1.5" dy="1.5" layer="1" cream="no"/>
<text x="-0.7501" y="0.8001" size="1.27" layer="25">&gt;NAME</text>
<text x="-0.762" y="-0.889" size="0.0254" layer="27">&gt;VALUE</text>
<text x="0" y="-2.54" size="1" layer="37">&gt;TP_SIGNAL_NAME</text>
</package>
<package name="TP16SQ" urn="urn:adsk.eagle:footprint:27933/1" library_version="3">
<description>&lt;b&gt;TEST PAD&lt;/b&gt;</description>
<smd name="TP" x="0" y="0" dx="1.5996" dy="1.5996" layer="1" cream="no"/>
<text x="-0.8001" y="0.8499" size="1.27" layer="25">&gt;NAME</text>
<text x="-0.762" y="-0.889" size="0.0254" layer="27">&gt;VALUE</text>
<text x="0" y="-2.54" size="1" layer="37">&gt;TP_SIGNAL_NAME</text>
</package>
<package name="TP17SQ" urn="urn:adsk.eagle:footprint:27934/1" library_version="3">
<description>&lt;b&gt;TEST PAD&lt;/b&gt;</description>
<smd name="TP" x="0" y="0" dx="1.7" dy="1.7" layer="1" cream="no"/>
<text x="-0.8499" y="0.8999" size="1.27" layer="25">&gt;NAME</text>
<text x="-0.762" y="-0.889" size="0.0254" layer="27">&gt;VALUE</text>
<text x="0" y="-2.54" size="1" layer="37">&gt;TP_SIGNAL_NAME</text>
</package>
<package name="TP18SQ" urn="urn:adsk.eagle:footprint:27935/1" library_version="3">
<description>&lt;b&gt;TEST PAD&lt;/b&gt;</description>
<smd name="TP" x="0" y="0" dx="1.8" dy="1.8" layer="1" cream="no"/>
<text x="-0.8999" y="0.95" size="1.27" layer="25">&gt;NAME</text>
<text x="-0.889" y="-1.016" size="0.0254" layer="27">&gt;VALUE</text>
<text x="0" y="-2.54" size="1" layer="37">&gt;TP_SIGNAL_NAME</text>
</package>
<package name="TP19SQ" urn="urn:adsk.eagle:footprint:27936/1" library_version="3">
<description>&lt;b&gt;TEST PAD&lt;/b&gt;</description>
<smd name="TP" x="0" y="0" dx="1.8998" dy="1.8998" layer="1" cream="no"/>
<text x="-0.95" y="1" size="1.27" layer="25">&gt;NAME</text>
<text x="-0.889" y="-1.016" size="0.0254" layer="27">&gt;VALUE</text>
<text x="0" y="-2.54" size="1" layer="37">&gt;TP_SIGNAL_NAME</text>
</package>
<package name="TP20SQ" urn="urn:adsk.eagle:footprint:27937/1" library_version="3">
<description>&lt;b&gt;TEST PAD&lt;/b&gt;</description>
<smd name="TP" x="0" y="0" dx="2" dy="2" layer="1" cream="no"/>
<text x="-1" y="1.05" size="1.27" layer="25">&gt;NAME</text>
<text x="-1.016" y="-1.143" size="0.0254" layer="27">&gt;VALUE</text>
<text x="0" y="-2.54" size="1" layer="37">&gt;TP_SIGNAL_NAME</text>
</package>
</packages>
<packages3d>
<package3d name="B1,27" urn="urn:adsk.eagle:package:27944/2" type="box" library_version="3">
<description>TEST PAD</description>
<packageinstances>
<packageinstance name="B1,27"/>
</packageinstances>
</package3d>
<package3d name="B2,54" urn="urn:adsk.eagle:package:27948/1" type="box" library_version="3">
<description>TEST PAD</description>
<packageinstances>
<packageinstance name="B2,54"/>
</packageinstances>
</package3d>
<package3d name="P1-13" urn="urn:adsk.eagle:package:27946/1" type="box" library_version="3">
<description>TEST PAD</description>
<packageinstances>
<packageinstance name="P1-13"/>
</packageinstances>
</package3d>
<package3d name="P1-13Y" urn="urn:adsk.eagle:package:27947/1" type="box" library_version="3">
<description>TEST PAD</description>
<packageinstances>
<packageinstance name="P1-13Y"/>
</packageinstances>
</package3d>
<package3d name="P1-17" urn="urn:adsk.eagle:package:27949/1" type="box" library_version="3">
<description>TEST PAD</description>
<packageinstances>
<packageinstance name="P1-17"/>
</packageinstances>
</package3d>
<package3d name="P1-17Y" urn="urn:adsk.eagle:package:27953/1" type="box" library_version="3">
<description>TEST PAD</description>
<packageinstances>
<packageinstance name="P1-17Y"/>
</packageinstances>
</package3d>
<package3d name="P1-20" urn="urn:adsk.eagle:package:27950/1" type="box" library_version="3">
<description>TEST PAD</description>
<packageinstances>
<packageinstance name="P1-20"/>
</packageinstances>
</package3d>
<package3d name="P1-20Y" urn="urn:adsk.eagle:package:27951/1" type="box" library_version="3">
<description>TEST PAD</description>
<packageinstances>
<packageinstance name="P1-20Y"/>
</packageinstances>
</package3d>
<package3d name="TP06R" urn="urn:adsk.eagle:package:27954/1" type="box" library_version="3">
<description>TEST PAD</description>
<packageinstances>
<packageinstance name="TP06R"/>
</packageinstances>
</package3d>
<package3d name="TP06SQ" urn="urn:adsk.eagle:package:27952/1" type="box" library_version="3">
<description>TEST PAD</description>
<packageinstances>
<packageinstance name="TP06SQ"/>
</packageinstances>
</package3d>
<package3d name="TP07R" urn="urn:adsk.eagle:package:27970/1" type="box" library_version="3">
<description>TEST PAD</description>
<packageinstances>
<packageinstance name="TP07R"/>
</packageinstances>
</package3d>
<package3d name="TP07SQ" urn="urn:adsk.eagle:package:27955/1" type="box" library_version="3">
<description>TEST PAD</description>
<packageinstances>
<packageinstance name="TP07SQ"/>
</packageinstances>
</package3d>
<package3d name="TP08R" urn="urn:adsk.eagle:package:27956/1" type="box" library_version="3">
<description>TEST PAD</description>
<packageinstances>
<packageinstance name="TP08R"/>
</packageinstances>
</package3d>
<package3d name="TP08SQ" urn="urn:adsk.eagle:package:27960/1" type="box" library_version="3">
<description>TEST PAD</description>
<packageinstances>
<packageinstance name="TP08SQ"/>
</packageinstances>
</package3d>
<package3d name="TP09R" urn="urn:adsk.eagle:package:27958/1" type="box" library_version="3">
<description>TEST PAD</description>
<packageinstances>
<packageinstance name="TP09R"/>
</packageinstances>
</package3d>
<package3d name="TP09SQ" urn="urn:adsk.eagle:package:27957/1" type="box" library_version="3">
<description>TEST PAD</description>
<packageinstances>
<packageinstance name="TP09SQ"/>
</packageinstances>
</package3d>
<package3d name="TP10R" urn="urn:adsk.eagle:package:27959/1" type="box" library_version="3">
<description>TEST PAD</description>
<packageinstances>
<packageinstance name="TP10R"/>
</packageinstances>
</package3d>
<package3d name="TP10SQ" urn="urn:adsk.eagle:package:27962/1" type="box" library_version="3">
<description>TEST PAD</description>
<packageinstances>
<packageinstance name="TP10SQ"/>
</packageinstances>
</package3d>
<package3d name="TP11R" urn="urn:adsk.eagle:package:27961/1" type="box" library_version="3">
<description>TEST PAD</description>
<packageinstances>
<packageinstance name="TP11R"/>
</packageinstances>
</package3d>
<package3d name="TP11SQ" urn="urn:adsk.eagle:package:27965/1" type="box" library_version="3">
<description>TEST PAD</description>
<packageinstances>
<packageinstance name="TP11SQ"/>
</packageinstances>
</package3d>
<package3d name="TP12SQ" urn="urn:adsk.eagle:package:27964/1" type="box" library_version="3">
<description>TEST PAD</description>
<packageinstances>
<packageinstance name="TP12SQ"/>
</packageinstances>
</package3d>
<package3d name="TP12R" urn="urn:adsk.eagle:package:27963/1" type="box" library_version="3">
<description>TEST PAD</description>
<packageinstances>
<packageinstance name="TP12R"/>
</packageinstances>
</package3d>
<package3d name="TP13R" urn="urn:adsk.eagle:package:27967/1" type="box" library_version="3">
<description>TEST PAD</description>
<packageinstances>
<packageinstance name="TP13R"/>
</packageinstances>
</package3d>
<package3d name="TP14R" urn="urn:adsk.eagle:package:27966/1" type="box" library_version="3">
<description>TEST PAD</description>
<packageinstances>
<packageinstance name="TP14R"/>
</packageinstances>
</package3d>
<package3d name="TP15R" urn="urn:adsk.eagle:package:27968/1" type="box" library_version="3">
<description>TEST PAD</description>
<packageinstances>
<packageinstance name="TP15R"/>
</packageinstances>
</package3d>
<package3d name="TP16R" urn="urn:adsk.eagle:package:27969/1" type="box" library_version="3">
<description>TEST PAD</description>
<packageinstances>
<packageinstance name="TP16R"/>
</packageinstances>
</package3d>
<package3d name="TP17R" urn="urn:adsk.eagle:package:27971/1" type="box" library_version="3">
<description>TEST PAD</description>
<packageinstances>
<packageinstance name="TP17R"/>
</packageinstances>
</package3d>
<package3d name="TP18R" urn="urn:adsk.eagle:package:27981/1" type="box" library_version="3">
<description>TEST PAD</description>
<packageinstances>
<packageinstance name="TP18R"/>
</packageinstances>
</package3d>
<package3d name="TP19R" urn="urn:adsk.eagle:package:27972/1" type="box" library_version="3">
<description>TEST PAD</description>
<packageinstances>
<packageinstance name="TP19R"/>
</packageinstances>
</package3d>
<package3d name="TP20R" urn="urn:adsk.eagle:package:27973/1" type="box" library_version="3">
<description>TEST PAD</description>
<packageinstances>
<packageinstance name="TP20R"/>
</packageinstances>
</package3d>
<package3d name="TP13SQ" urn="urn:adsk.eagle:package:27974/1" type="box" library_version="3">
<description>TEST PAD</description>
<packageinstances>
<packageinstance name="TP13SQ"/>
</packageinstances>
</package3d>
<package3d name="TP14SQ" urn="urn:adsk.eagle:package:27984/1" type="box" library_version="3">
<description>TEST PAD</description>
<packageinstances>
<packageinstance name="TP14SQ"/>
</packageinstances>
</package3d>
<package3d name="TP15SQ" urn="urn:adsk.eagle:package:27975/1" type="box" library_version="3">
<description>TEST PAD</description>
<packageinstances>
<packageinstance name="TP15SQ"/>
</packageinstances>
</package3d>
<package3d name="TP16SQ" urn="urn:adsk.eagle:package:27976/1" type="box" library_version="3">
<description>TEST PAD</description>
<packageinstances>
<packageinstance name="TP16SQ"/>
</packageinstances>
</package3d>
<package3d name="TP17SQ" urn="urn:adsk.eagle:package:27977/1" type="box" library_version="3">
<description>TEST PAD</description>
<packageinstances>
<packageinstance name="TP17SQ"/>
</packageinstances>
</package3d>
<package3d name="TP18SQ" urn="urn:adsk.eagle:package:27979/1" type="box" library_version="3">
<description>TEST PAD</description>
<packageinstances>
<packageinstance name="TP18SQ"/>
</packageinstances>
</package3d>
<package3d name="TP19SQ" urn="urn:adsk.eagle:package:27978/1" type="box" library_version="3">
<description>TEST PAD</description>
<packageinstances>
<packageinstance name="TP19SQ"/>
</packageinstances>
</package3d>
<package3d name="TP20SQ" urn="urn:adsk.eagle:package:27980/1" type="box" library_version="3">
<description>TEST PAD</description>
<packageinstances>
<packageinstance name="TP20SQ"/>
</packageinstances>
</package3d>
</packages3d>
<symbols>
<symbol name="TP" urn="urn:adsk.eagle:symbol:27940/1" library_version="3">
<wire x1="-0.762" y1="-0.762" x2="0" y2="0" width="0.254" layer="94"/>
<wire x1="0" y1="0" x2="0.762" y2="-0.762" width="0.254" layer="94"/>
<wire x1="0.762" y1="-0.762" x2="0" y2="-1.524" width="0.254" layer="94"/>
<wire x1="0" y1="-1.524" x2="-0.762" y2="-0.762" width="0.254" layer="94"/>
<text x="-1.27" y="1.27" size="1.778" layer="95">&gt;NAME</text>
<text x="1.27" y="-1.27" size="1.778" layer="97">&gt;TP_SIGNAL_NAME</text>
<pin name="TP" x="0" y="-2.54" visible="off" length="short" direction="in" rot="R90"/>
</symbol>
</symbols>
<devicesets>
<deviceset name="TP" urn="urn:adsk.eagle:component:27992/3" prefix="TP" library_version="3">
<description>&lt;b&gt;Test pad&lt;/b&gt;</description>
<gates>
<gate name="G$1" symbol="TP" x="0" y="0"/>
</gates>
<devices>
<device name="B1,27" package="B1,27">
<connects>
<connect gate="G$1" pin="TP" pad="TP"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:27944/2"/>
</package3dinstances>
<technologies>
<technology name="">
<attribute name="POPULARITY" value="19" constant="no"/>
<attribute name="TP_SIGNAL_NAME" value="" constant="no"/>
</technology>
</technologies>
</device>
<device name="B2,54" package="B2,54">
<connects>
<connect gate="G$1" pin="TP" pad="TP"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:27948/1"/>
</package3dinstances>
<technologies>
<technology name="">
<attribute name="POPULARITY" value="3" constant="no"/>
<attribute name="TP_SIGNAL_NAME" value="" constant="no"/>
</technology>
</technologies>
</device>
<device name="PAD1-13" package="P1-13">
<connects>
<connect gate="G$1" pin="TP" pad="TP"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:27946/1"/>
</package3dinstances>
<technologies>
<technology name="">
<attribute name="POPULARITY" value="12" constant="no"/>
<attribute name="TP_SIGNAL_NAME" value="" constant="no"/>
</technology>
</technologies>
</device>
<device name="PAD1-13Y" package="P1-13Y">
<connects>
<connect gate="G$1" pin="TP" pad="TP"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:27947/1"/>
</package3dinstances>
<technologies>
<technology name="">
<attribute name="POPULARITY" value="0" constant="no"/>
<attribute name="TP_SIGNAL_NAME" value="" constant="no"/>
</technology>
</technologies>
</device>
<device name="PAD1-17" package="P1-17">
<connects>
<connect gate="G$1" pin="TP" pad="TP"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:27949/1"/>
</package3dinstances>
<technologies>
<technology name="">
<attribute name="POPULARITY" value="0" constant="no"/>
<attribute name="TP_SIGNAL_NAME" value="" constant="no"/>
</technology>
</technologies>
</device>
<device name="PAD1-17Y" package="P1-17Y">
<connects>
<connect gate="G$1" pin="TP" pad="TP"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:27953/1"/>
</package3dinstances>
<technologies>
<technology name="">
<attribute name="POPULARITY" value="3" constant="no"/>
<attribute name="TP_SIGNAL_NAME" value="" constant="no"/>
</technology>
</technologies>
</device>
<device name="PAD1-20" package="P1-20">
<connects>
<connect gate="G$1" pin="TP" pad="TP"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:27950/1"/>
</package3dinstances>
<technologies>
<technology name="">
<attribute name="POPULARITY" value="0" constant="no"/>
<attribute name="TP_SIGNAL_NAME" value="" constant="no"/>
</technology>
</technologies>
</device>
<device name="PAD1-20Y" package="P1-20Y">
<connects>
<connect gate="G$1" pin="TP" pad="TP"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:27951/1"/>
</package3dinstances>
<technologies>
<technology name="">
<attribute name="POPULARITY" value="0" constant="no"/>
<attribute name="TP_SIGNAL_NAME" value="" constant="no"/>
</technology>
</technologies>
</device>
<device name="TP06R" package="TP06R">
<connects>
<connect gate="G$1" pin="TP" pad="TP"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:27954/1"/>
</package3dinstances>
<technologies>
<technology name="">
<attribute name="POPULARITY" value="1" constant="no"/>
<attribute name="TP_SIGNAL_NAME" value="" constant="no"/>
</technology>
</technologies>
</device>
<device name="TP06SQ" package="TP06SQ">
<connects>
<connect gate="G$1" pin="TP" pad="TP"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:27952/1"/>
</package3dinstances>
<technologies>
<technology name="">
<attribute name="POPULARITY" value="0" constant="no"/>
<attribute name="TP_SIGNAL_NAME" value="" constant="no"/>
</technology>
</technologies>
</device>
<device name="TP07R" package="TP07R">
<connects>
<connect gate="G$1" pin="TP" pad="TP"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:27970/1"/>
</package3dinstances>
<technologies>
<technology name="">
<attribute name="POPULARITY" value="0" constant="no"/>
<attribute name="TP_SIGNAL_NAME" value="" constant="no"/>
</technology>
</technologies>
</device>
<device name="TP07SQ" package="TP07SQ">
<connects>
<connect gate="G$1" pin="TP" pad="TP"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:27955/1"/>
</package3dinstances>
<technologies>
<technology name="">
<attribute name="POPULARITY" value="0" constant="no"/>
<attribute name="TP_SIGNAL_NAME" value="" constant="no"/>
</technology>
</technologies>
</device>
<device name="TP08R" package="TP08R">
<connects>
<connect gate="G$1" pin="TP" pad="TP"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:27956/1"/>
</package3dinstances>
<technologies>
<technology name="">
<attribute name="POPULARITY" value="0" constant="no"/>
<attribute name="TP_SIGNAL_NAME" value="" constant="no"/>
</technology>
</technologies>
</device>
<device name="TP08SQ" package="TP08SQ">
<connects>
<connect gate="G$1" pin="TP" pad="TP"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:27960/1"/>
</package3dinstances>
<technologies>
<technology name="">
<attribute name="POPULARITY" value="0" constant="no"/>
<attribute name="TP_SIGNAL_NAME" value="" constant="no"/>
</technology>
</technologies>
</device>
<device name="TP09R" package="TP09R">
<connects>
<connect gate="G$1" pin="TP" pad="TP"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:27958/1"/>
</package3dinstances>
<technologies>
<technology name="">
<attribute name="POPULARITY" value="0" constant="no"/>
<attribute name="TP_SIGNAL_NAME" value="" constant="no"/>
</technology>
</technologies>
</device>
<device name="TP09SQ" package="TP09SQ">
<connects>
<connect gate="G$1" pin="TP" pad="TP"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:27957/1"/>
</package3dinstances>
<technologies>
<technology name="">
<attribute name="POPULARITY" value="0" constant="no"/>
<attribute name="TP_SIGNAL_NAME" value="" constant="no"/>
</technology>
</technologies>
</device>
<device name="TP10R" package="TP10R">
<connects>
<connect gate="G$1" pin="TP" pad="TP"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:27959/1"/>
</package3dinstances>
<technologies>
<technology name="">
<attribute name="POPULARITY" value="3" constant="no"/>
<attribute name="TP_SIGNAL_NAME" value="" constant="no"/>
</technology>
</technologies>
</device>
<device name="TP10SQ" package="TP10SQ">
<connects>
<connect gate="G$1" pin="TP" pad="TP"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:27962/1"/>
</package3dinstances>
<technologies>
<technology name="">
<attribute name="POPULARITY" value="4" constant="no"/>
<attribute name="TP_SIGNAL_NAME" value="" constant="no"/>
</technology>
</technologies>
</device>
<device name="TP11R" package="TP11R">
<connects>
<connect gate="G$1" pin="TP" pad="TP"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:27961/1"/>
</package3dinstances>
<technologies>
<technology name="">
<attribute name="POPULARITY" value="1" constant="no"/>
<attribute name="TP_SIGNAL_NAME" value="" constant="no"/>
</technology>
</technologies>
</device>
<device name="TP11SQ" package="TP11SQ">
<connects>
<connect gate="G$1" pin="TP" pad="TP"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:27965/1"/>
</package3dinstances>
<technologies>
<technology name="">
<attribute name="POPULARITY" value="0" constant="no"/>
<attribute name="TP_SIGNAL_NAME" value="" constant="no"/>
</technology>
</technologies>
</device>
<device name="TP12SQ" package="TP12SQ">
<connects>
<connect gate="G$1" pin="TP" pad="TP"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:27964/1"/>
</package3dinstances>
<technologies>
<technology name="">
<attribute name="POPULARITY" value="0" constant="no"/>
<attribute name="TP_SIGNAL_NAME" value="" constant="no"/>
</technology>
</technologies>
</device>
<device name="TP12R" package="TP12R">
<connects>
<connect gate="G$1" pin="TP" pad="TP"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:27963/1"/>
</package3dinstances>
<technologies>
<technology name="">
<attribute name="POPULARITY" value="1" constant="no"/>
<attribute name="TP_SIGNAL_NAME" value="" constant="no"/>
</technology>
</technologies>
</device>
<device name="TP13R" package="TP13R">
<connects>
<connect gate="G$1" pin="TP" pad="TP"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:27967/1"/>
</package3dinstances>
<technologies>
<technology name="">
<attribute name="POPULARITY" value="0" constant="no"/>
<attribute name="TP_SIGNAL_NAME" value="" constant="no"/>
</technology>
</technologies>
</device>
<device name="TP14R" package="TP14R">
<connects>
<connect gate="G$1" pin="TP" pad="TP"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:27966/1"/>
</package3dinstances>
<technologies>
<technology name="">
<attribute name="POPULARITY" value="0" constant="no"/>
<attribute name="TP_SIGNAL_NAME" value="" constant="no"/>
</technology>
</technologies>
</device>
<device name="TP15R" package="TP15R">
<connects>
<connect gate="G$1" pin="TP" pad="TP"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:27968/1"/>
</package3dinstances>
<technologies>
<technology name="">
<attribute name="POPULARITY" value="0" constant="no"/>
<attribute name="TP_SIGNAL_NAME" value="" constant="no"/>
</technology>
</technologies>
</device>
<device name="TP16R" package="TP16R">
<connects>
<connect gate="G$1" pin="TP" pad="TP"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:27969/1"/>
</package3dinstances>
<technologies>
<technology name="">
<attribute name="POPULARITY" value="0" constant="no"/>
<attribute name="TP_SIGNAL_NAME" value="" constant="no"/>
</technology>
</technologies>
</device>
<device name="TP17R" package="TP17R">
<connects>
<connect gate="G$1" pin="TP" pad="TP"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:27971/1"/>
</package3dinstances>
<technologies>
<technology name="">
<attribute name="POPULARITY" value="0" constant="no"/>
<attribute name="TP_SIGNAL_NAME" value="" constant="no"/>
</technology>
</technologies>
</device>
<device name="TP18R" package="TP18R">
<connects>
<connect gate="G$1" pin="TP" pad="TP"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:27981/1"/>
</package3dinstances>
<technologies>
<technology name="">
<attribute name="POPULARITY" value="0" constant="no"/>
<attribute name="TP_SIGNAL_NAME" value="" constant="no"/>
</technology>
</technologies>
</device>
<device name="TP19R" package="TP19R">
<connects>
<connect gate="G$1" pin="TP" pad="TP"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:27972/1"/>
</package3dinstances>
<technologies>
<technology name="">
<attribute name="POPULARITY" value="0" constant="no"/>
<attribute name="TP_SIGNAL_NAME" value="" constant="no"/>
</technology>
</technologies>
</device>
<device name="TP20R" package="TP20R">
<connects>
<connect gate="G$1" pin="TP" pad="TP"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:27973/1"/>
</package3dinstances>
<technologies>
<technology name="">
<attribute name="POPULARITY" value="1" constant="no"/>
<attribute name="TP_SIGNAL_NAME" value="" constant="no"/>
</technology>
</technologies>
</device>
<device name="TP13SQ" package="TP13SQ">
<connects>
<connect gate="G$1" pin="TP" pad="TP"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:27974/1"/>
</package3dinstances>
<technologies>
<technology name="">
<attribute name="POPULARITY" value="0" constant="no"/>
<attribute name="TP_SIGNAL_NAME" value="" constant="no"/>
</technology>
</technologies>
</device>
<device name="TP14SQ" package="TP14SQ">
<connects>
<connect gate="G$1" pin="TP" pad="TP"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:27984/1"/>
</package3dinstances>
<technologies>
<technology name="">
<attribute name="POPULARITY" value="0" constant="no"/>
<attribute name="TP_SIGNAL_NAME" value="" constant="no"/>
</technology>
</technologies>
</device>
<device name="TP15SQ" package="TP15SQ">
<connects>
<connect gate="G$1" pin="TP" pad="TP"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:27975/1"/>
</package3dinstances>
<technologies>
<technology name="">
<attribute name="POPULARITY" value="0" constant="no"/>
<attribute name="TP_SIGNAL_NAME" value="" constant="no"/>
</technology>
</technologies>
</device>
<device name="TP16SQ" package="TP16SQ">
<connects>
<connect gate="G$1" pin="TP" pad="TP"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:27976/1"/>
</package3dinstances>
<technologies>
<technology name="">
<attribute name="POPULARITY" value="0" constant="no"/>
<attribute name="TP_SIGNAL_NAME" value="" constant="no"/>
</technology>
</technologies>
</device>
<device name="TP17SQ" package="TP17SQ">
<connects>
<connect gate="G$1" pin="TP" pad="TP"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:27977/1"/>
</package3dinstances>
<technologies>
<technology name="">
<attribute name="POPULARITY" value="0" constant="no"/>
<attribute name="TP_SIGNAL_NAME" value="" constant="no"/>
</technology>
</technologies>
</device>
<device name="TP18SQ" package="TP18SQ">
<connects>
<connect gate="G$1" pin="TP" pad="TP"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:27979/1"/>
</package3dinstances>
<technologies>
<technology name="">
<attribute name="POPULARITY" value="0" constant="no"/>
<attribute name="TP_SIGNAL_NAME" value="" constant="no"/>
</technology>
</technologies>
</device>
<device name="TP19SQ" package="TP19SQ">
<connects>
<connect gate="G$1" pin="TP" pad="TP"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:27978/1"/>
</package3dinstances>
<technologies>
<technology name="">
<attribute name="POPULARITY" value="0" constant="no"/>
<attribute name="TP_SIGNAL_NAME" value="" constant="no"/>
</technology>
</technologies>
</device>
<device name="TP20SQ" package="TP20SQ">
<connects>
<connect gate="G$1" pin="TP" pad="TP"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:27980/1"/>
</package3dinstances>
<technologies>
<technology name="">
<attribute name="POPULARITY" value="2" constant="no"/>
<attribute name="TP_SIGNAL_NAME" value="" constant="no"/>
</technology>
</technologies>
</device>
</devices>
</deviceset>
</devicesets>
</library>
<library name="pinhead" urn="urn:adsk.eagle:library:325">
<description>&lt;b&gt;Pin Header Connectors&lt;/b&gt;&lt;p&gt;
&lt;author&gt;Created by librarian@cadsoft.de&lt;/author&gt;</description>
<packages>
<package name="1X04" urn="urn:adsk.eagle:footprint:22258/1" library_version="4">
<description>&lt;b&gt;PIN HEADER&lt;/b&gt;</description>
<wire x1="0" y1="0.635" x2="0.635" y2="1.27" width="0.1524" layer="21"/>
<wire x1="0.635" y1="1.27" x2="1.905" y2="1.27" width="0.1524" layer="21"/>
<wire x1="1.905" y1="1.27" x2="2.54" y2="0.635" width="0.1524" layer="21"/>
<wire x1="2.54" y1="0.635" x2="2.54" y2="-0.635" width="0.1524" layer="21"/>
<wire x1="2.54" y1="-0.635" x2="1.905" y2="-1.27" width="0.1524" layer="21"/>
<wire x1="1.905" y1="-1.27" x2="0.635" y2="-1.27" width="0.1524" layer="21"/>
<wire x1="0.635" y1="-1.27" x2="0" y2="-0.635" width="0.1524" layer="21"/>
<wire x1="-4.445" y1="1.27" x2="-3.175" y2="1.27" width="0.1524" layer="21"/>
<wire x1="-3.175" y1="1.27" x2="-2.54" y2="0.635" width="0.1524" layer="21"/>
<wire x1="-2.54" y1="0.635" x2="-2.54" y2="-0.635" width="0.1524" layer="21"/>
<wire x1="-2.54" y1="-0.635" x2="-3.175" y2="-1.27" width="0.1524" layer="21"/>
<wire x1="-2.54" y1="0.635" x2="-1.905" y2="1.27" width="0.1524" layer="21"/>
<wire x1="-1.905" y1="1.27" x2="-0.635" y2="1.27" width="0.1524" layer="21"/>
<wire x1="-0.635" y1="1.27" x2="0" y2="0.635" width="0.1524" layer="21"/>
<wire x1="0" y1="0.635" x2="0" y2="-0.635" width="0.1524" layer="21"/>
<wire x1="0" y1="-0.635" x2="-0.635" y2="-1.27" width="0.1524" layer="21"/>
<wire x1="-0.635" y1="-1.27" x2="-1.905" y2="-1.27" width="0.1524" layer="21"/>
<wire x1="-1.905" y1="-1.27" x2="-2.54" y2="-0.635" width="0.1524" layer="21"/>
<wire x1="-5.08" y1="0.635" x2="-5.08" y2="-0.635" width="0.1524" layer="21"/>
<wire x1="-4.445" y1="1.27" x2="-5.08" y2="0.635" width="0.1524" layer="21"/>
<wire x1="-5.08" y1="-0.635" x2="-4.445" y2="-1.27" width="0.1524" layer="21"/>
<wire x1="-3.175" y1="-1.27" x2="-4.445" y2="-1.27" width="0.1524" layer="21"/>
<wire x1="3.175" y1="1.27" x2="4.445" y2="1.27" width="0.1524" layer="21"/>
<wire x1="4.445" y1="1.27" x2="5.08" y2="0.635" width="0.1524" layer="21"/>
<wire x1="5.08" y1="0.635" x2="5.08" y2="-0.635" width="0.1524" layer="21"/>
<wire x1="5.08" y1="-0.635" x2="4.445" y2="-1.27" width="0.1524" layer="21"/>
<wire x1="3.175" y1="1.27" x2="2.54" y2="0.635" width="0.1524" layer="21"/>
<wire x1="2.54" y1="-0.635" x2="3.175" y2="-1.27" width="0.1524" layer="21"/>
<wire x1="4.445" y1="-1.27" x2="3.175" y2="-1.27" width="0.1524" layer="21"/>
<pad name="1" x="-3.81" y="0" drill="1.016" shape="long" rot="R90"/>
<pad name="2" x="-1.27" y="0" drill="1.016" shape="long" rot="R90"/>
<pad name="3" x="1.27" y="0" drill="1.016" shape="long" rot="R90"/>
<pad name="4" x="3.81" y="0" drill="1.016" shape="long" rot="R90"/>
<text x="-5.1562" y="1.8288" size="1.27" layer="25" ratio="10">&gt;NAME</text>
<text x="-5.08" y="-3.175" size="1.27" layer="27">&gt;VALUE</text>
<rectangle x1="1.016" y1="-0.254" x2="1.524" y2="0.254" layer="51"/>
<rectangle x1="-1.524" y1="-0.254" x2="-1.016" y2="0.254" layer="51"/>
<rectangle x1="-4.064" y1="-0.254" x2="-3.556" y2="0.254" layer="51"/>
<rectangle x1="3.556" y1="-0.254" x2="4.064" y2="0.254" layer="51"/>
</package>
<package name="1X04/90" urn="urn:adsk.eagle:footprint:22259/1" library_version="4">
<description>&lt;b&gt;PIN HEADER&lt;/b&gt;</description>
<wire x1="-5.08" y1="-1.905" x2="-2.54" y2="-1.905" width="0.1524" layer="21"/>
<wire x1="-2.54" y1="-1.905" x2="-2.54" y2="0.635" width="0.1524" layer="21"/>
<wire x1="-2.54" y1="0.635" x2="-5.08" y2="0.635" width="0.1524" layer="21"/>
<wire x1="-5.08" y1="0.635" x2="-5.08" y2="-1.905" width="0.1524" layer="21"/>
<wire x1="-3.81" y1="6.985" x2="-3.81" y2="1.27" width="0.762" layer="21"/>
<wire x1="-2.54" y1="-1.905" x2="0" y2="-1.905" width="0.1524" layer="21"/>
<wire x1="0" y1="-1.905" x2="0" y2="0.635" width="0.1524" layer="21"/>
<wire x1="0" y1="0.635" x2="-2.54" y2="0.635" width="0.1524" layer="21"/>
<wire x1="-1.27" y1="6.985" x2="-1.27" y2="1.27" width="0.762" layer="21"/>
<wire x1="0" y1="-1.905" x2="2.54" y2="-1.905" width="0.1524" layer="21"/>
<wire x1="2.54" y1="-1.905" x2="2.54" y2="0.635" width="0.1524" layer="21"/>
<wire x1="2.54" y1="0.635" x2="0" y2="0.635" width="0.1524" layer="21"/>
<wire x1="1.27" y1="6.985" x2="1.27" y2="1.27" width="0.762" layer="21"/>
<wire x1="2.54" y1="-1.905" x2="5.08" y2="-1.905" width="0.1524" layer="21"/>
<wire x1="5.08" y1="-1.905" x2="5.08" y2="0.635" width="0.1524" layer="21"/>
<wire x1="5.08" y1="0.635" x2="2.54" y2="0.635" width="0.1524" layer="21"/>
<wire x1="3.81" y1="6.985" x2="3.81" y2="1.27" width="0.762" layer="21"/>
<pad name="1" x="-3.81" y="-3.81" drill="1.016" shape="long" rot="R90"/>
<pad name="2" x="-1.27" y="-3.81" drill="1.016" shape="long" rot="R90"/>
<pad name="3" x="1.27" y="-3.81" drill="1.016" shape="long" rot="R90"/>
<pad name="4" x="3.81" y="-3.81" drill="1.016" shape="long" rot="R90"/>
<text x="-5.715" y="-3.81" size="1.27" layer="25" ratio="10" rot="R90">&gt;NAME</text>
<text x="6.985" y="-4.445" size="1.27" layer="27" rot="R90">&gt;VALUE</text>
<rectangle x1="-4.191" y1="0.635" x2="-3.429" y2="1.143" layer="21"/>
<rectangle x1="-1.651" y1="0.635" x2="-0.889" y2="1.143" layer="21"/>
<rectangle x1="0.889" y1="0.635" x2="1.651" y2="1.143" layer="21"/>
<rectangle x1="3.429" y1="0.635" x2="4.191" y2="1.143" layer="21"/>
<rectangle x1="-4.191" y1="-2.921" x2="-3.429" y2="-1.905" layer="21"/>
<rectangle x1="-1.651" y1="-2.921" x2="-0.889" y2="-1.905" layer="21"/>
<rectangle x1="0.889" y1="-2.921" x2="1.651" y2="-1.905" layer="21"/>
<rectangle x1="3.429" y1="-2.921" x2="4.191" y2="-1.905" layer="21"/>
</package>
<package name="1X01" urn="urn:adsk.eagle:footprint:22382/1" library_version="4">
<description>&lt;b&gt;PIN HEADER&lt;/b&gt;</description>
<wire x1="-0.635" y1="1.27" x2="0.635" y2="1.27" width="0.1524" layer="21"/>
<wire x1="0.635" y1="1.27" x2="1.27" y2="0.635" width="0.1524" layer="21"/>
<wire x1="1.27" y1="0.635" x2="1.27" y2="-0.635" width="0.1524" layer="21"/>
<wire x1="1.27" y1="-0.635" x2="0.635" y2="-1.27" width="0.1524" layer="21"/>
<wire x1="-1.27" y1="0.635" x2="-1.27" y2="-0.635" width="0.1524" layer="21"/>
<wire x1="-0.635" y1="1.27" x2="-1.27" y2="0.635" width="0.1524" layer="21"/>
<wire x1="-1.27" y1="-0.635" x2="-0.635" y2="-1.27" width="0.1524" layer="21"/>
<wire x1="0.635" y1="-1.27" x2="-0.635" y2="-1.27" width="0.1524" layer="21"/>
<pad name="1" x="0" y="0" drill="1.016" shape="octagon"/>
<text x="-1.3462" y="1.8288" size="1.27" layer="25" ratio="10">&gt;NAME</text>
<text x="-1.27" y="-3.175" size="1.27" layer="27">&gt;VALUE</text>
<rectangle x1="-0.254" y1="-0.254" x2="0.254" y2="0.254" layer="51"/>
</package>
</packages>
<packages3d>
<package3d name="1X04" urn="urn:adsk.eagle:package:22407/2" type="model" library_version="4">
<description>PIN HEADER</description>
<packageinstances>
<packageinstance name="1X04"/>
</packageinstances>
</package3d>
<package3d name="1X04/90" urn="urn:adsk.eagle:package:22404/2" type="model" library_version="4">
<description>PIN HEADER</description>
<packageinstances>
<packageinstance name="1X04/90"/>
</packageinstances>
</package3d>
<package3d name="1X01" urn="urn:adsk.eagle:package:22485/2" type="model" library_version="4">
<description>PIN HEADER</description>
<packageinstances>
<packageinstance name="1X01"/>
</packageinstances>
</package3d>
</packages3d>
<symbols>
<symbol name="PINHD4" urn="urn:adsk.eagle:symbol:22257/1" library_version="4">
<wire x1="-6.35" y1="-5.08" x2="1.27" y2="-5.08" width="0.4064" layer="94"/>
<wire x1="1.27" y1="-5.08" x2="1.27" y2="7.62" width="0.4064" layer="94"/>
<wire x1="1.27" y1="7.62" x2="-6.35" y2="7.62" width="0.4064" layer="94"/>
<wire x1="-6.35" y1="7.62" x2="-6.35" y2="-5.08" width="0.4064" layer="94"/>
<text x="-6.35" y="8.255" size="1.778" layer="95">&gt;NAME</text>
<text x="-6.35" y="-7.62" size="1.778" layer="96">&gt;VALUE</text>
<pin name="1" x="-2.54" y="5.08" visible="pad" length="short" direction="pas" function="dot"/>
<pin name="2" x="-2.54" y="2.54" visible="pad" length="short" direction="pas" function="dot"/>
<pin name="3" x="-2.54" y="0" visible="pad" length="short" direction="pas" function="dot"/>
<pin name="4" x="-2.54" y="-2.54" visible="pad" length="short" direction="pas" function="dot"/>
</symbol>
<symbol name="PINHD1" urn="urn:adsk.eagle:symbol:22381/1" library_version="4">
<wire x1="-6.35" y1="-2.54" x2="1.27" y2="-2.54" width="0.4064" layer="94"/>
<wire x1="1.27" y1="-2.54" x2="1.27" y2="2.54" width="0.4064" layer="94"/>
<wire x1="1.27" y1="2.54" x2="-6.35" y2="2.54" width="0.4064" layer="94"/>
<wire x1="-6.35" y1="2.54" x2="-6.35" y2="-2.54" width="0.4064" layer="94"/>
<text x="-6.35" y="3.175" size="1.778" layer="95">&gt;NAME</text>
<text x="-6.35" y="-5.08" size="1.778" layer="96">&gt;VALUE</text>
<pin name="1" x="-2.54" y="0" visible="pad" length="short" direction="pas" function="dot"/>
</symbol>
</symbols>
<devicesets>
<deviceset name="PINHD-1X4" urn="urn:adsk.eagle:component:22499/5" prefix="JP" uservalue="yes" library_version="4">
<description>&lt;b&gt;PIN HEADER&lt;/b&gt;</description>
<gates>
<gate name="A" symbol="PINHD4" x="0" y="0"/>
</gates>
<devices>
<device name="" package="1X04">
<connects>
<connect gate="A" pin="1" pad="1"/>
<connect gate="A" pin="2" pad="2"/>
<connect gate="A" pin="3" pad="3"/>
<connect gate="A" pin="4" pad="4"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:22407/2"/>
</package3dinstances>
<technologies>
<technology name="">
<attribute name="POPULARITY" value="91" constant="no"/>
</technology>
</technologies>
</device>
<device name="/90" package="1X04/90">
<connects>
<connect gate="A" pin="1" pad="1"/>
<connect gate="A" pin="2" pad="2"/>
<connect gate="A" pin="3" pad="3"/>
<connect gate="A" pin="4" pad="4"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:22404/2"/>
</package3dinstances>
<technologies>
<technology name="">
<attribute name="POPULARITY" value="9" constant="no"/>
</technology>
</technologies>
</device>
</devices>
</deviceset>
<deviceset name="PINHD-1X1" urn="urn:adsk.eagle:component:22540/3" prefix="JP" uservalue="yes" library_version="4">
<description>&lt;b&gt;PIN HEADER&lt;/b&gt;</description>
<gates>
<gate name="G$1" symbol="PINHD1" x="0" y="0"/>
</gates>
<devices>
<device name="" package="1X01">
<connects>
<connect gate="G$1" pin="1" pad="1"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:22485/2"/>
</package3dinstances>
<technologies>
<technology name="">
<attribute name="POPULARITY" value="64" constant="no"/>
</technology>
</technologies>
</device>
</devices>
</deviceset>
</devicesets>
</library>
<library name="PCA9674ABS,118">
<packages>
<package name="PCA9674ABS,118">
<rectangle x1="-0.47" y1="-0.47" x2="0.47" y2="0.47" layer="31"/>
<text x="-2.41" y="-3.115" size="1.27" layer="27" align="top-left">&gt;VALUE</text>
<text x="-2.41" y="3.115" size="1.27" layer="25">&gt;NAME</text>
<circle x="-2.495" y="0.75" radius="0.1" width="0.2" layer="21"/>
<circle x="-2.495" y="0.75" radius="0.1" width="0.2" layer="51"/>
<wire x1="1.55" y1="-1.55" x2="-1.55" y2="-1.55" width="0.127" layer="51"/>
<wire x1="1.55" y1="1.55" x2="-1.55" y2="1.55" width="0.127" layer="51"/>
<wire x1="1.55" y1="-1.55" x2="1.55" y2="1.55" width="0.127" layer="51"/>
<wire x1="-1.55" y1="-1.55" x2="-1.55" y2="1.55" width="0.127" layer="51"/>
<wire x1="1.55" y1="-1.55" x2="1.2" y2="-1.55" width="0.127" layer="21"/>
<wire x1="1.55" y1="1.55" x2="1.2" y2="1.55" width="0.127" layer="21"/>
<wire x1="-1.55" y1="-1.55" x2="-1.2" y2="-1.55" width="0.127" layer="21"/>
<wire x1="-1.55" y1="1.55" x2="-1.2" y2="1.55" width="0.127" layer="21"/>
<wire x1="1.55" y1="-1.55" x2="1.55" y2="-1.2" width="0.127" layer="21"/>
<wire x1="1.55" y1="1.55" x2="1.55" y2="1.2" width="0.127" layer="21"/>
<wire x1="-1.55" y1="-1.55" x2="-1.55" y2="-1.2" width="0.127" layer="21"/>
<wire x1="-1.55" y1="1.55" x2="-1.55" y2="1.2" width="0.127" layer="21"/>
<wire x1="-2.115" y1="-2.115" x2="2.115" y2="-2.115" width="0.05" layer="39"/>
<wire x1="-2.115" y1="2.115" x2="2.115" y2="2.115" width="0.05" layer="39"/>
<wire x1="-2.115" y1="-2.115" x2="-2.115" y2="2.115" width="0.05" layer="39"/>
<wire x1="2.115" y1="-2.115" x2="2.115" y2="2.115" width="0.05" layer="39"/>
<smd name="5" x="-0.75" y="-1.435" dx="0.86" dy="0.26" layer="1" roundness="25" rot="R90"/>
<smd name="6" x="-0.25" y="-1.435" dx="0.86" dy="0.26" layer="1" roundness="25" rot="R90"/>
<smd name="7" x="0.25" y="-1.435" dx="0.86" dy="0.26" layer="1" roundness="25" rot="R90"/>
<smd name="8" x="0.75" y="-1.435" dx="0.86" dy="0.26" layer="1" roundness="25" rot="R90"/>
<smd name="13" x="0.75" y="1.435" dx="0.86" dy="0.26" layer="1" roundness="25" rot="R90"/>
<smd name="14" x="0.25" y="1.435" dx="0.86" dy="0.26" layer="1" roundness="25" rot="R90"/>
<smd name="15" x="-0.25" y="1.435" dx="0.86" dy="0.26" layer="1" roundness="25" rot="R90"/>
<smd name="16" x="-0.75" y="1.435" dx="0.86" dy="0.26" layer="1" roundness="25" rot="R90"/>
<smd name="1" x="-1.435" y="0.75" dx="0.86" dy="0.26" layer="1" roundness="25"/>
<smd name="2" x="-1.435" y="0.25" dx="0.86" dy="0.26" layer="1" roundness="25"/>
<smd name="3" x="-1.435" y="-0.25" dx="0.86" dy="0.26" layer="1" roundness="25"/>
<smd name="4" x="-1.435" y="-0.75" dx="0.86" dy="0.26" layer="1" roundness="25"/>
<smd name="9" x="1.435" y="-0.75" dx="0.86" dy="0.26" layer="1" roundness="25"/>
<smd name="10" x="1.435" y="-0.25" dx="0.86" dy="0.26" layer="1" roundness="25"/>
<smd name="11" x="1.435" y="0.25" dx="0.86" dy="0.26" layer="1" roundness="25"/>
<smd name="12" x="1.435" y="0.75" dx="0.86" dy="0.26" layer="1" roundness="25"/>
<smd name="17" x="0" y="0" dx="1.5" dy="1.5" layer="1" cream="no"/>
</package>
</packages>
<symbols>
<symbol name="PCA9674ABS,118">
<pin name="VDD" x="-15.24" y="7.62" length="middle"/>
<pin name="A0" x="-15.24" y="5.08" length="middle"/>
<pin name="A1" x="-15.24" y="2.54" length="middle"/>
<pin name="A2" x="-15.24" y="0" length="middle"/>
<pin name="SCL" x="-15.24" y="-2.54" length="middle"/>
<pin name="SDA" x="-15.24" y="-5.08" length="middle"/>
<pin name="!INT" x="-15.24" y="-7.62" length="middle"/>
<pin name="VSS" x="-15.24" y="-10.16" length="middle"/>
<pin name="P0" x="15.24" y="7.62" length="middle" rot="R180"/>
<pin name="P1" x="15.24" y="5.08" length="middle" rot="R180"/>
<pin name="P2" x="15.24" y="2.54" length="middle" rot="R180"/>
<pin name="P3" x="15.24" y="0" length="middle" rot="R180"/>
<pin name="P4" x="15.24" y="-2.54" length="middle" rot="R180"/>
<pin name="P5" x="15.24" y="-5.08" length="middle" rot="R180"/>
<pin name="P6" x="15.24" y="-7.62" length="middle" rot="R180"/>
<pin name="P7" x="15.24" y="-10.16" length="middle" rot="R180"/>
<wire x1="-10.16" y1="10.16" x2="10.16" y2="10.16" width="0.254" layer="94"/>
<wire x1="10.16" y1="10.16" x2="10.16" y2="-12.7" width="0.254" layer="94"/>
<wire x1="10.16" y1="-12.7" x2="-10.16" y2="-12.7" width="0.254" layer="94"/>
<wire x1="-10.16" y1="-12.7" x2="-10.16" y2="10.16" width="0.254" layer="94"/>
<text x="0" y="10.414" size="1.778" layer="95" align="bottom-center">&gt;NAME</text>
<text x="0" y="-12.954" size="1.778" layer="96" align="top-center">&gt;VALUE</text>
</symbol>
</symbols>
<devicesets>
<deviceset name="PCA9674ABS,118" prefix="U">
<gates>
<gate name="G$1" symbol="PCA9674ABS,118" x="0" y="0"/>
</gates>
<devices>
<device name="" package="PCA9674ABS,118">
<connects>
<connect gate="G$1" pin="!INT" pad="11"/>
<connect gate="G$1" pin="A0" pad="15"/>
<connect gate="G$1" pin="A1" pad="16"/>
<connect gate="G$1" pin="A2" pad="1"/>
<connect gate="G$1" pin="P0" pad="2"/>
<connect gate="G$1" pin="P1" pad="3"/>
<connect gate="G$1" pin="P2" pad="4"/>
<connect gate="G$1" pin="P3" pad="5"/>
<connect gate="G$1" pin="P4" pad="7"/>
<connect gate="G$1" pin="P5" pad="8"/>
<connect gate="G$1" pin="P6" pad="9"/>
<connect gate="G$1" pin="P7" pad="10"/>
<connect gate="G$1" pin="SCL" pad="12"/>
<connect gate="G$1" pin="SDA" pad="13"/>
<connect gate="G$1" pin="VDD" pad="14"/>
<connect gate="G$1" pin="VSS" pad="6 17"/>
</connects>
<technologies>
<technology name="">
<attribute name="A_MAX" value="1.0"/>
<attribute name="BALL_COLUMNS" value=""/>
<attribute name="BALL_ROWS" value=""/>
<attribute name="BODY_DIAMETER" value=""/>
<attribute name="B_MAX" value="0.3"/>
<attribute name="B_MIN" value="0.18"/>
<attribute name="B_NOM" value="0.24"/>
<attribute name="D2_NOM" value="1.5"/>
<attribute name="DMAX" value=""/>
<attribute name="DMIN" value=""/>
<attribute name="DNOM" value=""/>
<attribute name="D_MAX" value="3.1"/>
<attribute name="D_MIN" value="2.9"/>
<attribute name="D_NOM" value="3.0"/>
<attribute name="E2_NOM" value="1.5"/>
<attribute name="EMAX" value=""/>
<attribute name="EMIN" value=""/>
<attribute name="ENOM" value="0.5"/>
<attribute name="E_MAX" value="3.1"/>
<attribute name="E_MIN" value="2.9"/>
<attribute name="E_NOM" value="3.0"/>
<attribute name="IPC" value=""/>
<attribute name="JEDEC" value=""/>
<attribute name="L_MAX" value="0.5"/>
<attribute name="L_MIN" value="0.3"/>
<attribute name="L_NOM" value="0.4"/>
<attribute name="MANUFACTURER" value="NXP USA"/>
<attribute name="PACKAGE_TYPE" value=""/>
<attribute name="PINS" value=""/>
<attribute name="PIN_COLUMNS" value=""/>
<attribute name="PIN_COUNT_D" value="4.0"/>
<attribute name="PIN_COUNT_E" value="4.0"/>
<attribute name="SNAPEDA_PACKAGE_ID" value="5149"/>
<attribute name="STANDARD" value="IPC 7351B"/>
<attribute name="THERMAL_PAD" value=""/>
<attribute name="VACANCIES" value=""/>
</technology>
</technologies>
</device>
</devices>
</deviceset>
</devicesets>
</library>
<library name="0-Custom-Opto">
<packages>
<package name="CHIP-LED0603" urn="urn:adsk.eagle:footprint:15671/1" locally_modified="yes">
<description>&lt;b&gt;Hyper CHIPLED Hyper-Bright LED&lt;/b&gt;&lt;p&gt;
LB Q993&lt;br&gt;
Source: http://www.osram.convergy.de/ ... Lb_q993.pdf</description>
<wire x1="-0.4" y1="0.45" x2="-0.4" y2="-0.45" width="0.1016" layer="51"/>
<wire x1="0.4" y1="0.45" x2="0.4" y2="-0.45" width="0.1016" layer="51"/>
<smd name="C" x="0" y="0.75" dx="0.8" dy="0.8" layer="1"/>
<smd name="A" x="0" y="-0.75" dx="0.8" dy="0.8" layer="1"/>
<text x="-0.635" y="-0.635" size="1.27" layer="25" rot="R90">&gt;NAME</text>
<text x="1.905" y="-0.635" size="1.27" layer="27" rot="R90">&gt;VALUE</text>
<rectangle x1="-0.45" y1="0.45" x2="0.45" y2="0.85" layer="51"/>
<rectangle x1="-0.45" y1="-0.85" x2="0.45" y2="-0.45" layer="51"/>
<rectangle x1="-0.45" y1="0" x2="-0.3" y2="0.3" layer="21"/>
<rectangle x1="0.3" y1="0" x2="0.45" y2="0.3" layer="21"/>
<rectangle x1="-0.15" y1="0" x2="0.15" y2="0.3" layer="21"/>
<wire x1="-0.762" y1="-1.397" x2="-0.762" y2="1.397" width="0.127" layer="39"/>
<wire x1="-0.762" y1="1.397" x2="0.762" y2="1.397" width="0.127" layer="39"/>
<wire x1="0.762" y1="1.397" x2="0.762" y2="-1.397" width="0.127" layer="39"/>
<wire x1="0.762" y1="-1.397" x2="-0.762" y2="-1.397" width="0.127" layer="39"/>
</package>
</packages>
<packages3d>
<package3d name="CHIP-LED0603" urn="urn:adsk.eagle:package:15819/3" type="model">
<description>Hyper CHIPLED Hyper-Bright LED
LB Q993
Source: http://www.osram.convergy.de/ ... Lb_q993.pdf</description>
<packageinstances>
<packageinstance name="CHIP-LED0603"/>
</packageinstances>
</package3d>
</packages3d>
<symbols>
<symbol name="LED">
<wire x1="1.27" y1="0" x2="0" y2="-2.54" width="0.254" layer="94"/>
<wire x1="0" y1="-2.54" x2="-1.27" y2="0" width="0.254" layer="94"/>
<wire x1="1.27" y1="-2.54" x2="0" y2="-2.54" width="0.254" layer="94"/>
<wire x1="0" y1="-2.54" x2="-1.27" y2="-2.54" width="0.254" layer="94"/>
<wire x1="1.27" y1="0" x2="0" y2="0" width="0.254" layer="94"/>
<wire x1="0" y1="0" x2="-1.27" y2="0" width="0.254" layer="94"/>
<wire x1="-2.032" y1="-0.762" x2="-3.429" y2="-2.159" width="0.1524" layer="94"/>
<wire x1="-1.905" y1="-1.905" x2="-3.302" y2="-3.302" width="0.1524" layer="94"/>
<text x="3.556" y="-4.572" size="1.778" layer="95" rot="R90">&gt;NAME</text>
<text x="5.715" y="-4.572" size="1.778" layer="96" rot="R90">&gt;VALUE</text>
<pin name="C" x="0" y="-5.08" visible="off" length="short" direction="pas" rot="R90"/>
<pin name="A" x="0" y="2.54" visible="off" length="short" direction="pas" rot="R270"/>
<polygon width="0.1524" layer="94">
<vertex x="-3.429" y="-2.159"/>
<vertex x="-3.048" y="-1.27"/>
<vertex x="-2.54" y="-1.778"/>
</polygon>
<polygon width="0.1524" layer="94">
<vertex x="-3.302" y="-3.302"/>
<vertex x="-2.921" y="-2.413"/>
<vertex x="-2.413" y="-2.921"/>
</polygon>
</symbol>
</symbols>
<devicesets>
<deviceset name="LED,SMD,GREEN,0603" prefix="D" uservalue="yes">
<gates>
<gate name="G$1" symbol="LED" x="0" y="0"/>
</gates>
<devices>
<device name="CHIP-LED0603" package="CHIP-LED0603">
<connects>
<connect gate="G$1" pin="A" pad="A"/>
<connect gate="G$1" pin="C" pad="C"/>
</connects>
<package3dinstances>
<package3dinstance package3d_urn="urn:adsk.eagle:package:15819/3"/>
</package3dinstances>
<technologies>
<technology name=""/>
</technologies>
</device>
</devices>
</deviceset>
</devicesets>
</library>
</libraries>
<attributes>
</attributes>
<variantdefs>
</variantdefs>
<classes>
<class number="0" name="default" width="0" drill="0">
</class>
</classes>
<parts>
<part name="FRAME1" library="Custom-Frames" deviceset="A4L-LOC" device="">
<attribute name="NOTE" value="Engineers: Matthew Davidsen"/>
<attribute name="SHEET_NAME" value="Front End"/>
</part>
<part name="U1" library="AD8232ACPZ-R7" deviceset="AD8232ACPZ-R7" device=""/>
<part name="U2" library="ADS1219IPWR" deviceset="ADS1219IPWR" device=""/>
<part name="R1" library="0-Standard-Passives" deviceset="RES,SMD,10MOHM,1%,1/10W,0402" device="" package3d_urn="urn:adsk.eagle:package:23547/3" value="10Mohm"/>
<part name="R2" library="0-Standard-Passives" deviceset="RES,SMD,10MOHM,1%,1/10W,0402" device="" package3d_urn="urn:adsk.eagle:package:23547/3" value="10Mohm"/>
<part name="R3" library="0-Standard-Passives" deviceset="RES,SMD,182KOHM,1%,1/10W,0402" device="" package3d_urn="urn:adsk.eagle:package:23547/3" value="182kohm"/>
<part name="R4" library="0-Standard-Passives" deviceset="RES,SMD,182KOHM,1%,1/10W,0402" device="" package3d_urn="urn:adsk.eagle:package:23547/3" value="182kohm"/>
<part name="R5" library="0-Standard-Passives" deviceset="RES,SMD,10MOHM,1%,1/10W,0402" device="" package3d_urn="urn:adsk.eagle:package:23547/3" value="10Mohm"/>
<part name="R6" library="0-Standard-Passives" deviceset="RES,SMD,100KOHM,10%,1/10W,0402" device="" package3d_urn="urn:adsk.eagle:package:23547/3" value="100kohm"/>
<part name="R7" library="0-Standard-Passives" deviceset="RES,SMD,1MOHM,1%,1/10W,0402" device="" package3d_urn="urn:adsk.eagle:package:23547/3" value="1Mohm"/>
<part name="R8" library="0-Standard-Passives" deviceset="RES,SMD,100KOHM,10%,1/10W,0402" device="" package3d_urn="urn:adsk.eagle:package:23547/3" value="100kohm"/>
<part name="R9" library="0-Standard-Passives" deviceset="RES,SMD,649KOHM,1%,1/10W,0402" device="" package3d_urn="urn:adsk.eagle:package:23547/3" value="649kohm"/>
<part name="R10" library="0-Standard-Passives" deviceset="RES,SMD,649KOHM,1%,1/10W,0402" device="" package3d_urn="urn:adsk.eagle:package:23547/3" value="649kohm"/>
<part name="R11" library="0-Standard-Passives" deviceset="RES,SMD,10MOHM,1%,1/10W,0402" device="" package3d_urn="urn:adsk.eagle:package:23547/3" value="10Mohm"/>
<part name="R12" library="0-Standard-Passives" deviceset="RES,SMD,10MOHM,1%,1/10W,0402" device="" package3d_urn="urn:adsk.eagle:package:23547/3" value="10Mohm"/>
<part name="FRAME2" library="Custom-Frames" deviceset="A4L-LOC" device="">
<attribute name="NOTE" value="Engineers: Matthew Davidsen"/>
<attribute name="SHEET_NAME" value="ADC, GPIO, and Connector"/>
</part>
<part name="C2" library="0-Standard-Passives" deviceset="CAP,CER,1UF,10V,10%,X5R,0402" device="" value="1uF"/>
<part name="C3" library="0-Standard-Passives" deviceset="CAP,CER,1UF,10V,10%,X5R,0402" device="" value="1uF"/>
<part name="C4" library="0-Standard-Passives" deviceset="CAP,CER,6.2NF,25V,10%,X7R,0402" device="" value="6.2nF"/>
<part name="C5" library="0-Standard-Passives" deviceset="CAP,CER,1000PF,2KV,10%,X7R,0402" device="" value="1000pF"/>
<part name="C6" library="0-Standard-Passives" deviceset="CAP,CER,1UF,10V,10%,X5R,0402" device="" value="1uF"/>
<part name="C7" library="0-Standard-Passives" deviceset="CAP,CER,0.1UF,16V,10%,X5R,0402" device="" value="0.1uF"/>
<part name="U$1" library="0-Custom-Markers" deviceset="GND" device=""/>
<part name="C1" library="0-Standard-Passives" deviceset="CAP,CER,1000PF,2KV,10%,X7R,0402" device="" value="1000pF"/>
<part name="R13" library="0-Standard-Passives" deviceset="RES,SMD,0OHM,5%,1/16W,0402" device="" package3d_urn="urn:adsk.eagle:package:23547/3" value="0ohm"/>
<part name="R14" library="0-Standard-Passives" deviceset="RES,SMD,0OHM,5%,1/16W,0402" device="" package3d_urn="urn:adsk.eagle:package:23547/3" value="0ohm"/>
<part name="R15" library="0-Standard-Passives" deviceset="RES,SMD,0OHM,5%,1/16W,0402" device="" package3d_urn="urn:adsk.eagle:package:23547/3" value="0ohm"/>
<part name="R17" library="0-Standard-Passives" deviceset="RES,SMD,0OHM,5%,1/16W,0402" device="" package3d_urn="urn:adsk.eagle:package:23547/3" value="0ohm"/>
<part name="R18" library="0-Standard-Passives" deviceset="RES,SMD,0OHM,5%,1/16W,0402" device="" package3d_urn="urn:adsk.eagle:package:23547/3" value="0ohm"/>
<part name="U$5" library="0-Custom-Markers" deviceset="OFF-PAGE" device=""/>
<part name="U$7" library="0-Custom-Markers" deviceset="GND" device=""/>
<part name="U$8" library="0-Custom-Markers" deviceset="GND" device=""/>
<part name="U$9" library="0-Custom-Markers" deviceset="GND" device=""/>
<part name="U$11" library="0-Custom-Markers" deviceset="V-RAIL" device=""/>
<part name="R19" library="0-Standard-Passives" deviceset="RES,SMD,10KOHM,1%,1/16W,0402" device="" package3d_urn="urn:adsk.eagle:package:23547/3" value="10kohm"/>
<part name="R20" library="0-Standard-Passives" deviceset="RES,SMD,10KOHM,1%,1/16W,0402" device="" package3d_urn="urn:adsk.eagle:package:23547/3" value="10kohm"/>
<part name="R21" library="0-Standard-Passives" deviceset="RES,SMD,10KOHM,1%,1/16W,0402" device="" package3d_urn="urn:adsk.eagle:package:23547/3" value="10kohm"/>
<part name="R22" library="0-Standard-Passives" deviceset="RES,SMD,10KOHM,1%,1/16W,0402" device="" package3d_urn="urn:adsk.eagle:package:23547/3" value="10kohm"/>
<part name="U$10" library="0-Custom-Markers" deviceset="V-RAIL" device=""/>
<part name="U$13" library="0-Custom-Markers" deviceset="GND" device=""/>
<part name="U$14" library="0-Custom-Markers" deviceset="GND" device=""/>
<part name="C8" library="0-Standard-Passives" deviceset="CAP,CER,0.1UF,16V,10%,X5R,0402" device="" value="0.1uF"/>
<part name="C9" library="0-Standard-Passives" deviceset="CAP,CER,0.1UF,16V,10%,X5R,0402" device="" value="0.1uF"/>
<part name="U$15" library="0-Custom-Markers" deviceset="GND" device=""/>
<part name="U$16" library="0-Custom-Markers" deviceset="GND" device=""/>
<part name="U$17" library="0-Custom-Markers" deviceset="V-RAIL" device=""/>
<part name="U$18" library="0-Custom-Markers" deviceset="V-RAIL" device=""/>
<part name="R23" library="0-Standard-Passives" deviceset="RES,SMD,10KOHM,1%,1/16W,0402" device="" package3d_urn="urn:adsk.eagle:package:23547/3" value="10kohm"/>
<part name="U$21" library="0-Custom-Markers" deviceset="ON-PAGE" device=""/>
<part name="U$26" library="0-Custom-Markers" deviceset="GND" device=""/>
<part name="U$19" library="0-Custom-Markers" deviceset="V-RAIL" device=""/>
<part name="U$20" library="0-Custom-Markers" deviceset="GND" device=""/>
<part name="JP1" library="pinhead" library_urn="urn:adsk.eagle:library:325" deviceset="PINHD-1X4" device="" package3d_urn="urn:adsk.eagle:package:22407/2"/>
<part name="U$24" library="0-Custom-Markers" deviceset="ON-PAGE" device=""/>
<part name="U$3" library="0-Custom-Markers" deviceset="ON-PAGE" device=""/>
<part name="U$4" library="0-Custom-Markers" deviceset="ON-PAGE" device=""/>
<part name="U$25" library="0-Custom-Markers" deviceset="ON-PAGE" device=""/>
<part name="JP2" library="pinhead" library_urn="urn:adsk.eagle:library:325" deviceset="PINHD-1X1" device="" package3d_urn="urn:adsk.eagle:package:22485/2"/>
<part name="JP3" library="pinhead" library_urn="urn:adsk.eagle:library:325" deviceset="PINHD-1X1" device="" package3d_urn="urn:adsk.eagle:package:22485/2"/>
<part name="U$28" library="0-Custom-Markers" deviceset="GND" device=""/>
<part name="U$29" library="0-Custom-Markers" deviceset="V-RAIL" device=""/>
<part name="U$12" library="0-Custom-Markers" deviceset="V-RAIL" device=""/>
<part name="U$2" library="0-Custom-Markers" deviceset="ON-PAGE" device=""/>
<part name="U$6" library="0-Custom-Markers" deviceset="OFF-PAGE" device=""/>
<part name="U$23" library="0-Custom-Markers" deviceset="OFF-PAGE" device=""/>
<part name="U3" library="PCA9674ABS,118" deviceset="PCA9674ABS,118" device=""/>
<part name="C10" library="0-Standard-Passives" deviceset="CAP,CER,0.1UF,16V,10%,X5R,0402" device="" value="0.1uF"/>
<part name="R24" library="0-Standard-Passives" deviceset="RES,SMD,10KOHM,1%,1/16W,0402" device="" package3d_urn="urn:adsk.eagle:package:23547/3" value="10kohm"/>
<part name="R25" library="0-Standard-Passives" deviceset="RES,SMD,10KOHM,1%,1/16W,0402" device="" package3d_urn="urn:adsk.eagle:package:23547/3" value="10kohm"/>
<part name="R26" library="0-Standard-Passives" deviceset="RES,SMD,10KOHM,1%,1/16W,0402" device="" package3d_urn="urn:adsk.eagle:package:23547/3" value="10kohm"/>
<part name="R27" library="0-Standard-Passives" deviceset="RES,SMD,10KOHM,1%,1/16W,0402" device="" package3d_urn="urn:adsk.eagle:package:23547/3" value="10kohm"/>
<part name="R28" library="0-Standard-Passives" deviceset="RES,SMD,10KOHM,1%,1/16W,0402" device="" package3d_urn="urn:adsk.eagle:package:23547/3" value="10kohm"/>
<part name="R29" library="0-Standard-Passives" deviceset="RES,SMD,10KOHM,1%,1/16W,0402" device="" package3d_urn="urn:adsk.eagle:package:23547/3" value="10kohm"/>
<part name="U$27" library="0-Custom-Markers" deviceset="GND" device=""/>
<part name="U$30" library="0-Custom-Markers" deviceset="GND" device=""/>
<part name="U$31" library="0-Custom-Markers" deviceset="V-RAIL" device=""/>
<part name="U$32" library="0-Custom-Markers" deviceset="V-RAIL" device=""/>
<part name="TP1" library="testpad" library_urn="urn:adsk.eagle:library:385" deviceset="TP" device="B1,27" package3d_urn="urn:adsk.eagle:package:27944/2"/>
<part name="U$33" library="0-Custom-Markers" deviceset="GND" device=""/>
<part name="C11" library="0-Standard-Passives" deviceset="CAP,CER,0.1UF,16V,10%,X5R,0402" device="" value="0.1uF"/>
<part name="U$34" library="0-Custom-Markers" deviceset="GND" device=""/>
<part name="U$22" library="0-Custom-Markers" deviceset="ON-PAGE" device=""/>
<part name="TP4" library="testpad" library_urn="urn:adsk.eagle:library:385" deviceset="TP" device="B1,27" package3d_urn="urn:adsk.eagle:package:27944/2"/>
<part name="TP3" library="testpad" library_urn="urn:adsk.eagle:library:385" deviceset="TP" device="B1,27" package3d_urn="urn:adsk.eagle:package:27944/2"/>
<part name="R16" library="0-Standard-Passives" deviceset="RES,SMD,10KOHM,1%,1/16W,0402" device="" package3d_urn="urn:adsk.eagle:package:23547/3" value="10kohm"/>
<part name="U$35" library="0-Custom-Markers" deviceset="OFF-PAGE" device=""/>
<part name="U$36" library="0-Custom-Markers" deviceset="ON-PAGE" device=""/>
<part name="R30" library="0-Standard-Passives" deviceset="RES,SMD,10KOHM,1%,1/16W,0402" device="" package3d_urn="urn:adsk.eagle:package:23547/3" value="10kohm"/>
<part name="R31" library="0-Standard-Passives" deviceset="RES,SMD,10KOHM,1%,1/16W,0402" device="" package3d_urn="urn:adsk.eagle:package:23547/3" value="10kohm"/>
<part name="U$37" library="0-Custom-Markers" deviceset="V-RAIL" device=""/>
<part name="R32" library="0-Standard-Passives" deviceset="RES,SMD,0OHM,5%,1/16W,0402" device="" package3d_urn="urn:adsk.eagle:package:23547/3" value="0ohm"/>
<part name="R33" library="0-Standard-Passives" deviceset="RES,SMD,0OHM,5%,1/16W,0402" device="" package3d_urn="urn:adsk.eagle:package:23547/3" value="0ohm"/>
<part name="R34" library="0-Standard-Passives" deviceset="RES,SMD,0OHM,5%,1/16W,0402" device="" package3d_urn="urn:adsk.eagle:package:23547/3" value="0ohm"/>
<part name="R35" library="0-Standard-Passives" deviceset="RES,SMD,0OHM,5%,1/16W,0402" device="" package3d_urn="urn:adsk.eagle:package:23547/3" value="0ohm"/>
<part name="R36" library="0-Standard-Passives" deviceset="RES,SMD,100OHM,5%,1/10W,0402" device="" package3d_urn="urn:adsk.eagle:package:23547/3" value="100ohm"/>
<part name="D1" library="0-Custom-Opto" deviceset="LED,SMD,GREEN,0603" device="CHIP-LED0603" package3d_urn="urn:adsk.eagle:package:15819/3"/>
<part name="U$38" library="0-Custom-Markers" deviceset="GND" device=""/>
<part name="U$39" library="0-Custom-Markers" deviceset="OFF-PAGE" device=""/>
<part name="U$40" library="0-Custom-Markers" deviceset="ON-PAGE" device=""/>
</parts>
<sheets>
<sheet>
<plain>
<text x="192.024" y="83.82" size="1.778" layer="97" rot="R180">DNP</text>
<text x="199.644" y="83.82" size="1.778" layer="97" rot="R180">DNP</text>
</plain>
<instances>
<instance part="FRAME1" gate="G$1" x="0" y="0" smashed="yes">
<attribute name="DRAWING_NAME" x="217.17" y="15.24" size="2.54" layer="94"/>
<attribute name="LAST_DATE_TIME" x="217.17" y="10.16" size="2.286" layer="94"/>
<attribute name="SHEET" x="230.505" y="5.08" size="2.54" layer="94"/>
<attribute name="NOTE" x="163.83" y="20.32" size="2.286" layer="94"/>
<attribute name="SHEET_NAME" x="217.17" y="20.32" size="2.54" layer="94"/>
</instance>
<instance part="U1" gate="G$1" x="124.46" y="86.36" smashed="yes">
<attribute name="NAME" x="134.62" y="106.68" size="1.778" layer="95"/>
<attribute name="VALUE" x="134.62" y="66.04" size="1.778" layer="96" align="top-left"/>
</instance>
<instance part="R1" gate="G$1" x="50.8" y="76.2" smashed="yes" rot="R90">
<attribute name="NAME" x="49.3014" y="72.39" size="1.778" layer="95" rot="R90"/>
<attribute name="VALUE" x="54.102" y="72.39" size="1.778" layer="96" rot="R90"/>
</instance>
<instance part="R2" gate="G$1" x="58.42" y="76.2" smashed="yes" rot="R90">
<attribute name="NAME" x="56.9214" y="72.39" size="1.778" layer="95" rot="R90"/>
<attribute name="VALUE" x="61.722" y="72.39" size="1.778" layer="96" rot="R90"/>
</instance>
<instance part="R3" gate="G$1" x="76.2" y="91.44" smashed="yes" rot="R180">
<attribute name="NAME" x="80.01" y="89.9414" size="1.778" layer="95" rot="R180"/>
<attribute name="VALUE" x="80.01" y="94.742" size="1.778" layer="96" rot="R180"/>
</instance>
<instance part="R4" gate="G$1" x="76.2" y="86.36" smashed="yes">
<attribute name="NAME" x="72.39" y="87.8586" size="1.778" layer="95"/>
<attribute name="VALUE" x="72.39" y="83.058" size="1.778" layer="96"/>
</instance>
<instance part="R5" gate="G$1" x="78.74" y="114.3" smashed="yes">
<attribute name="NAME" x="74.93" y="115.7986" size="1.778" layer="95"/>
<attribute name="VALUE" x="74.93" y="110.998" size="1.778" layer="96"/>
</instance>
<instance part="R6" gate="G$1" x="114.3" y="25.4" smashed="yes" rot="R180">
<attribute name="NAME" x="118.11" y="23.9014" size="1.778" layer="95" rot="R180"/>
<attribute name="VALUE" x="118.11" y="28.702" size="1.778" layer="96" rot="R180"/>
</instance>
<instance part="R7" gate="G$1" x="180.34" y="48.26" smashed="yes" rot="R180">
<attribute name="NAME" x="184.15" y="46.7614" size="1.778" layer="95" rot="R180"/>
<attribute name="VALUE" x="184.15" y="51.562" size="1.778" layer="96" rot="R180"/>
</instance>
<instance part="R8" gate="G$1" x="165.1" y="48.26" smashed="yes" rot="R180">
<attribute name="NAME" x="168.91" y="46.7614" size="1.778" layer="95" rot="R180"/>
<attribute name="VALUE" x="168.91" y="51.562" size="1.778" layer="96" rot="R180"/>
</instance>
<instance part="R9" gate="G$1" x="121.92" y="40.64" smashed="yes" rot="R90">
<attribute name="NAME" x="120.4214" y="36.83" size="1.778" layer="95" rot="R90"/>
<attribute name="VALUE" x="125.222" y="36.83" size="1.778" layer="96" rot="R90"/>
</instance>
<instance part="R10" gate="G$1" x="114.3" y="33.02" smashed="yes" rot="R180">
<attribute name="NAME" x="118.11" y="31.5214" size="1.778" layer="95" rot="R180"/>
<attribute name="VALUE" x="118.11" y="36.322" size="1.778" layer="96" rot="R180"/>
</instance>
<instance part="R11" gate="G$1" x="111.76" y="154.94" smashed="yes" rot="R270">
<attribute name="NAME" x="113.2586" y="158.75" size="1.778" layer="95" rot="R270"/>
<attribute name="VALUE" x="108.458" y="158.75" size="1.778" layer="96" rot="R270"/>
</instance>
<instance part="R12" gate="G$1" x="111.76" y="137.16" smashed="yes" rot="R90">
<attribute name="NAME" x="110.2614" y="133.35" size="1.778" layer="95" rot="R90"/>
<attribute name="VALUE" x="115.062" y="133.35" size="1.778" layer="96" rot="R90"/>
</instance>
<instance part="C2" gate="G$1" x="88.9" y="104.14" smashed="yes">
<attribute name="NAME" x="90.424" y="104.521" size="1.778" layer="95"/>
<attribute name="VALUE" x="90.424" y="99.441" size="1.778" layer="96"/>
</instance>
<instance part="C3" gate="G$1" x="106.68" y="20.32" smashed="yes">
<attribute name="NAME" x="108.204" y="20.701" size="1.778" layer="95"/>
<attribute name="VALUE" x="108.204" y="15.621" size="1.778" layer="96"/>
</instance>
<instance part="C4" gate="G$1" x="147.32" y="48.26" smashed="yes" rot="R90">
<attribute name="NAME" x="146.939" y="49.784" size="1.778" layer="95" rot="R90"/>
<attribute name="VALUE" x="152.019" y="49.784" size="1.778" layer="96" rot="R90"/>
</instance>
<instance part="C5" gate="A" x="147.32" y="33.02" smashed="yes" rot="R90">
<attribute name="NAME" x="146.939" y="34.544" size="1.778" layer="95" rot="R90"/>
<attribute name="VALUE" x="152.019" y="34.544" size="1.778" layer="96" rot="R90"/>
</instance>
<instance part="C6" gate="G$1" x="101.6" y="142.24" smashed="yes">
<attribute name="NAME" x="103.124" y="142.621" size="1.778" layer="95"/>
<attribute name="VALUE" x="103.124" y="137.541" size="1.778" layer="96"/>
</instance>
<instance part="C7" gate="G$1" x="132.08" y="157.48" smashed="yes">
<attribute name="NAME" x="133.604" y="157.861" size="1.778" layer="95"/>
<attribute name="VALUE" x="133.604" y="152.781" size="1.778" layer="96"/>
</instance>
<instance part="U$1" gate="G$1" x="142.24" y="106.68" smashed="yes"/>
<instance part="C1" gate="A" x="86.36" y="73.66" smashed="yes" rot="R180">
<attribute name="NAME" x="84.836" y="73.279" size="1.778" layer="95" rot="R180"/>
<attribute name="VALUE" x="84.836" y="78.359" size="1.778" layer="96" rot="R180"/>
</instance>
<instance part="R13" gate="G$1" x="106.68" y="43.18" smashed="yes" rot="R90">
<attribute name="NAME" x="105.1814" y="39.37" size="1.778" layer="95" rot="R90"/>
<attribute name="VALUE" x="109.982" y="39.37" size="1.778" layer="96" rot="R90"/>
</instance>
<instance part="R14" gate="G$1" x="193.04" y="99.06" smashed="yes" rot="R90">
<attribute name="NAME" x="191.5414" y="95.25" size="1.778" layer="95" rot="R90"/>
<attribute name="VALUE" x="196.342" y="95.25" size="1.778" layer="96" rot="R90"/>
</instance>
<instance part="R15" gate="G$1" x="200.66" y="99.06" smashed="yes" rot="R90">
<attribute name="NAME" x="199.1614" y="95.25" size="1.778" layer="95" rot="R90"/>
<attribute name="VALUE" x="203.962" y="95.25" size="1.778" layer="96" rot="R90"/>
</instance>
<instance part="R17" gate="G$1" x="193.04" y="78.74" smashed="yes" rot="R90">
<attribute name="NAME" x="191.5414" y="74.93" size="1.778" layer="95" rot="R90"/>
<attribute name="VALUE" x="196.342" y="74.93" size="1.778" layer="96" rot="R90"/>
</instance>
<instance part="R18" gate="G$1" x="200.66" y="78.74" smashed="yes" rot="R90">
<attribute name="NAME" x="199.1614" y="74.93" size="1.778" layer="95" rot="R90"/>
<attribute name="VALUE" x="203.962" y="74.93" size="1.778" layer="96" rot="R90"/>
</instance>
<instance part="U$5" gate="G$1" x="205.74" y="48.26" smashed="yes"/>
<instance part="U$7" gate="G$1" x="101.6" y="132.08" smashed="yes"/>
<instance part="U$8" gate="G$1" x="111.76" y="127" smashed="yes"/>
<instance part="U$9" gate="G$1" x="132.08" y="147.32" smashed="yes"/>
<instance part="U$11" gate="G$1" x="132.08" y="165.1" smashed="yes"/>
<instance part="U$26" gate="G$1" x="200.66" y="66.04" smashed="yes"/>
<instance part="JP2" gate="G$1" x="35.56" y="93.98" smashed="yes" rot="R180">
<attribute name="NAME" x="41.91" y="90.805" size="1.778" layer="95" rot="R180"/>
<attribute name="VALUE" x="41.91" y="99.06" size="1.778" layer="96" rot="R180"/>
</instance>
<instance part="JP3" gate="G$1" x="35.56" y="83.82" smashed="yes" rot="R180">
<attribute name="NAME" x="41.91" y="80.645" size="1.778" layer="95" rot="R180"/>
<attribute name="VALUE" x="41.91" y="88.9" size="1.778" layer="96" rot="R180"/>
</instance>
<instance part="U$12" gate="G$1" x="200.66" y="109.22" smashed="yes"/>
<instance part="U$2" gate="G$1" x="167.64" y="86.36" smashed="yes" rot="R180"/>
<instance part="U$6" gate="G$1" x="167.64" y="83.82" smashed="yes"/>
<instance part="U$39" gate="G$1" x="167.64" y="81.28" smashed="yes"/>
</instances>
<busses>
</busses>
<nets>
<net name="HPDRIVE" class="0">
<segment>
<pinref part="U1" gate="G$1" pin="HPDRIVE"/>
<pinref part="C2" gate="G$1" pin="2"/>
<wire x1="101.6" y1="91.44" x2="88.9" y2="91.44" width="0.1524" layer="91"/>
<wire x1="88.9" y1="91.44" x2="88.9" y2="99.06" width="0.1524" layer="91"/>
<label x="88.9" y="91.694" size="1.778" layer="95"/>
</segment>
</net>
<net name="ECG-HPSENSE" class="0">
<segment>
<pinref part="C2" gate="G$1" pin="1"/>
<wire x1="88.9" y1="106.68" x2="88.9" y2="114.3" width="0.1524" layer="91"/>
<wire x1="88.9" y1="114.3" x2="119.38" y2="114.3" width="0.1524" layer="91"/>
<pinref part="U1" gate="G$1" pin="HPSENSE"/>
<label x="91.44" y="114.554" size="1.778" layer="95"/>
<wire x1="119.38" y1="109.22" x2="119.38" y2="114.3" width="0.1524" layer="91"/>
<pinref part="R5" gate="G$1" pin="2"/>
<wire x1="88.9" y1="114.3" x2="83.82" y2="114.3" width="0.1524" layer="91"/>
<junction x="88.9" y="114.3"/>
</segment>
</net>
<net name="ECG-IAOUT" class="0">
<segment>
<pinref part="C3" gate="G$1" pin="2"/>
<wire x1="106.68" y1="15.24" x2="106.68" y2="12.7" width="0.1524" layer="91"/>
<label x="91.44" y="12.954" size="1.778" layer="95"/>
<wire x1="106.68" y1="12.7" x2="15.24" y2="12.7" width="0.1524" layer="91"/>
<wire x1="15.24" y1="12.7" x2="15.24" y2="119.38" width="0.1524" layer="91"/>
<pinref part="U1" gate="G$1" pin="IAOUT"/>
<wire x1="121.92" y1="109.22" x2="121.92" y2="119.38" width="0.1524" layer="91"/>
<pinref part="R5" gate="G$1" pin="1"/>
<label x="101.6" y="119.634" size="1.778" layer="95"/>
<wire x1="15.24" y1="119.38" x2="68.58" y2="119.38" width="0.1524" layer="91"/>
<wire x1="68.58" y1="119.38" x2="121.92" y2="119.38" width="0.1524" layer="91"/>
<wire x1="73.66" y1="114.3" x2="68.58" y2="114.3" width="0.1524" layer="91"/>
<wire x1="68.58" y1="114.3" x2="68.58" y2="119.38" width="0.1524" layer="91"/>
<junction x="68.58" y="119.38"/>
</segment>
</net>
<net name="ECG-IN_N" class="0">
<segment>
<pinref part="R2" gate="G$1" pin="2"/>
<wire x1="58.42" y1="81.28" x2="58.42" y2="86.36" width="0.1524" layer="91"/>
<pinref part="R4" gate="G$1" pin="1"/>
<wire x1="58.42" y1="86.36" x2="71.12" y2="86.36" width="0.1524" layer="91"/>
<label x="58.42" y="86.614" size="1.778" layer="95"/>
<wire x1="58.42" y1="86.36" x2="45.72" y2="86.36" width="0.1524" layer="91"/>
<junction x="58.42" y="86.36"/>
<pinref part="JP3" gate="G$1" pin="1"/>
<wire x1="38.1" y1="83.82" x2="45.72" y2="83.82" width="0.1524" layer="91"/>
<wire x1="45.72" y1="83.82" x2="45.72" y2="86.36" width="0.1524" layer="91"/>
</segment>
</net>
<net name="ECG-IN-R_P" class="0">
<segment>
<pinref part="U1" gate="G$1" pin="IN+"/>
<pinref part="R3" gate="G$1" pin="1"/>
<label x="86.36" y="89.154" size="1.778" layer="95"/>
<wire x1="83.82" y1="88.9" x2="101.6" y2="88.9" width="0.1524" layer="91"/>
<wire x1="81.28" y1="91.44" x2="83.82" y2="91.44" width="0.1524" layer="91"/>
<wire x1="83.82" y1="91.44" x2="83.82" y2="88.9" width="0.1524" layer="91"/>
</segment>
</net>
<net name="ECG-RLD" class="0">
<segment>
<pinref part="R1" gate="G$1" pin="1"/>
<wire x1="50.8" y1="71.12" x2="50.8" y2="68.58" width="0.1524" layer="91"/>
<wire x1="50.8" y1="68.58" x2="58.42" y2="68.58" width="0.1524" layer="91"/>
<pinref part="R2" gate="G$1" pin="1"/>
<wire x1="58.42" y1="68.58" x2="58.42" y2="71.12" width="0.1524" layer="91"/>
<wire x1="58.42" y1="68.58" x2="86.36" y2="68.58" width="0.1524" layer="91"/>
<junction x="58.42" y="68.58"/>
<wire x1="86.36" y1="68.58" x2="96.52" y2="68.58" width="0.1524" layer="91"/>
<wire x1="96.52" y1="68.58" x2="96.52" y2="81.28" width="0.1524" layer="91"/>
<pinref part="U1" gate="G$1" pin="RLD"/>
<wire x1="96.52" y1="81.28" x2="101.6" y2="81.28" width="0.1524" layer="91"/>
<wire x1="86.36" y1="71.12" x2="86.36" y2="68.58" width="0.1524" layer="91"/>
<junction x="86.36" y="68.58"/>
<label x="66.04" y="68.834" size="1.778" layer="95"/>
<pinref part="C1" gate="A" pin="1"/>
</segment>
</net>
<net name="ECG-RLD-FB" class="0">
<segment>
<pinref part="U1" gate="G$1" pin="RLDFB"/>
<wire x1="101.6" y1="83.82" x2="86.36" y2="83.82" width="0.1524" layer="91"/>
<wire x1="86.36" y1="83.82" x2="86.36" y2="78.74" width="0.1524" layer="91"/>
<label x="86.36" y="84.074" size="1.778" layer="95"/>
<pinref part="C1" gate="A" pin="2"/>
</segment>
</net>
<net name="ECG-IN-R_N" class="0">
<segment>
<pinref part="R4" gate="G$1" pin="2"/>
<pinref part="U1" gate="G$1" pin="IN-"/>
<wire x1="81.28" y1="86.36" x2="101.6" y2="86.36" width="0.1524" layer="91"/>
<label x="86.36" y="86.614" size="1.778" layer="95"/>
</segment>
</net>
<net name="ECG-IN_P" class="0">
<segment>
<pinref part="R3" gate="G$1" pin="2"/>
<pinref part="R1" gate="G$1" pin="2"/>
<wire x1="50.8" y1="91.44" x2="50.8" y2="81.28" width="0.1524" layer="91"/>
<wire x1="50.8" y1="91.44" x2="71.12" y2="91.44" width="0.1524" layer="91"/>
<label x="55.88" y="91.694" size="1.778" layer="95"/>
<junction x="50.8" y="91.44"/>
<pinref part="JP2" gate="G$1" pin="1"/>
<wire x1="38.1" y1="93.98" x2="45.72" y2="93.98" width="0.1524" layer="91"/>
<wire x1="45.72" y1="93.98" x2="45.72" y2="91.44" width="0.1524" layer="91"/>
<wire x1="45.72" y1="91.44" x2="50.8" y2="91.44" width="0.1524" layer="91"/>
</segment>
</net>
<net name="ECG-SW-R" class="0">
<segment>
<pinref part="R10" gate="G$1" pin="2"/>
<wire x1="106.68" y1="33.02" x2="109.22" y2="33.02" width="0.1524" layer="91"/>
<wire x1="106.68" y1="33.02" x2="106.68" y2="25.4" width="0.1524" layer="91"/>
<wire x1="106.68" y1="25.4" x2="109.22" y2="25.4" width="0.1524" layer="91"/>
<pinref part="R6" gate="G$1" pin="2"/>
<label x="106.426" y="25.4" size="1.778" layer="95" rot="R90"/>
<pinref part="C3" gate="G$1" pin="1"/>
<wire x1="106.68" y1="22.86" x2="106.68" y2="25.4" width="0.1524" layer="91"/>
<junction x="106.68" y="25.4"/>
<pinref part="R13" gate="G$1" pin="1"/>
<wire x1="106.68" y1="33.02" x2="106.68" y2="38.1" width="0.1524" layer="91"/>
<junction x="106.68" y="33.02"/>
</segment>
</net>
<net name="ECG-AMP-R" class="0">
<segment>
<pinref part="R10" gate="G$1" pin="1"/>
<wire x1="119.38" y1="33.02" x2="121.92" y2="33.02" width="0.1524" layer="91"/>
<pinref part="R9" gate="G$1" pin="1"/>
<wire x1="121.92" y1="33.02" x2="121.92" y2="35.56" width="0.1524" layer="91"/>
<wire x1="121.92" y1="33.02" x2="144.78" y2="33.02" width="0.1524" layer="91"/>
<junction x="121.92" y="33.02"/>
<pinref part="C5" gate="A" pin="1"/>
<label x="124.46" y="33.274" size="1.778" layer="95"/>
</segment>
</net>
<net name="ECG-REFOUT" class="0">
<segment>
<pinref part="R6" gate="G$1" pin="1"/>
<wire x1="119.38" y1="25.4" x2="157.48" y2="25.4" width="0.1524" layer="91"/>
<wire x1="157.48" y1="25.4" x2="157.48" y2="48.26" width="0.1524" layer="91"/>
<pinref part="C4" gate="G$1" pin="2"/>
<wire x1="152.4" y1="48.26" x2="154.94" y2="48.26" width="0.1524" layer="91"/>
<wire x1="154.94" y1="48.26" x2="157.48" y2="48.26" width="0.1524" layer="91"/>
<wire x1="157.48" y1="48.26" x2="160.02" y2="48.26" width="0.1524" layer="91"/>
<junction x="157.48" y="48.26"/>
<pinref part="R8" gate="G$1" pin="2"/>
<pinref part="U1" gate="G$1" pin="REFOUT"/>
<wire x1="124.46" y1="63.5" x2="124.46" y2="55.88" width="0.1524" layer="91"/>
<wire x1="124.46" y1="55.88" x2="154.94" y2="55.88" width="0.1524" layer="91"/>
<wire x1="154.94" y1="55.88" x2="154.94" y2="48.26" width="0.1524" layer="91"/>
<junction x="154.94" y="48.26"/>
<label x="127" y="56.134" size="1.778" layer="95"/>
</segment>
</net>
<net name="ECG-OPAMP_P" class="0">
<segment>
<pinref part="R9" gate="G$1" pin="2"/>
<wire x1="121.92" y1="45.72" x2="121.92" y2="48.26" width="0.1524" layer="91"/>
<pinref part="C4" gate="G$1" pin="1"/>
<wire x1="121.92" y1="48.26" x2="144.78" y2="48.26" width="0.1524" layer="91"/>
<pinref part="U1" gate="G$1" pin="OPAMP+"/>
<wire x1="121.92" y1="63.5" x2="121.92" y2="48.26" width="0.1524" layer="91"/>
<junction x="121.92" y="48.26"/>
<label x="124.46" y="48.514" size="1.778" layer="95"/>
</segment>
</net>
<net name="ECG-OPAMP_N" class="0">
<segment>
<pinref part="R8" gate="G$1" pin="1"/>
<wire x1="170.18" y1="48.26" x2="172.72" y2="48.26" width="0.1524" layer="91"/>
<pinref part="R7" gate="G$1" pin="2"/>
<pinref part="U1" gate="G$1" pin="OPAMP-"/>
<wire x1="172.72" y1="48.26" x2="175.26" y2="48.26" width="0.1524" layer="91"/>
<wire x1="127" y1="63.5" x2="127" y2="58.42" width="0.1524" layer="91"/>
<wire x1="127" y1="58.42" x2="172.72" y2="58.42" width="0.1524" layer="91"/>
<wire x1="172.72" y1="58.42" x2="172.72" y2="48.26" width="0.1524" layer="91"/>
<junction x="172.72" y="48.26"/>
<label x="129.54" y="58.674" size="1.778" layer="95"/>
</segment>
</net>
<net name="ECG-OUT" class="0">
<segment>
<pinref part="R7" gate="G$1" pin="1"/>
<wire x1="185.42" y1="48.26" x2="187.96" y2="48.26" width="0.1524" layer="91"/>
<pinref part="C5" gate="A" pin="2"/>
<wire x1="187.96" y1="48.26" x2="187.96" y2="33.02" width="0.1524" layer="91"/>
<wire x1="187.96" y1="33.02" x2="152.4" y2="33.02" width="0.1524" layer="91"/>
<wire x1="187.96" y1="48.26" x2="190.5" y2="48.26" width="0.1524" layer="91"/>
<junction x="187.96" y="48.26"/>
<label x="193.04" y="48.514" size="1.778" layer="95"/>
<pinref part="U1" gate="G$1" pin="OUT"/>
<wire x1="190.5" y1="48.26" x2="205.74" y2="48.26" width="0.1524" layer="91"/>
<wire x1="129.54" y1="63.5" x2="129.54" y2="60.96" width="0.1524" layer="91"/>
<wire x1="129.54" y1="60.96" x2="190.5" y2="60.96" width="0.1524" layer="91"/>
<wire x1="190.5" y1="60.96" x2="190.5" y2="48.26" width="0.1524" layer="91"/>
<junction x="190.5" y="48.26"/>
<pinref part="U$5" gate="G$1" pin="OUT"/>
</segment>
</net>
<net name="ECG-LOD_P" class="0">
<segment>
<pinref part="U1" gate="G$1" pin="LOD+"/>
<wire x1="147.32" y1="83.82" x2="167.64" y2="83.82" width="0.1524" layer="91"/>
<label x="149.86" y="84.074" size="1.778" layer="95"/>
<pinref part="U$6" gate="G$1" pin="OUT"/>
</segment>
</net>
<net name="ECG-REF-IN" class="0">
<segment>
<pinref part="U1" gate="G$1" pin="REFIN"/>
<pinref part="R11" gate="G$1" pin="2"/>
<wire x1="124.46" y1="109.22" x2="124.46" y2="144.78" width="0.1524" layer="91"/>
<label x="111.76" y="145.034" size="1.778" layer="95"/>
<wire x1="111.76" y1="144.78" x2="124.46" y2="144.78" width="0.1524" layer="91"/>
<wire x1="111.76" y1="144.78" x2="111.76" y2="147.32" width="0.1524" layer="91"/>
<pinref part="R12" gate="G$1" pin="2"/>
<wire x1="111.76" y1="147.32" x2="111.76" y2="149.86" width="0.1524" layer="91"/>
<wire x1="111.76" y1="142.24" x2="111.76" y2="144.78" width="0.1524" layer="91"/>
<junction x="111.76" y="144.78"/>
<pinref part="C6" gate="G$1" pin="1"/>
<wire x1="101.6" y1="144.78" x2="101.6" y2="147.32" width="0.1524" layer="91"/>
<wire x1="101.6" y1="147.32" x2="111.76" y2="147.32" width="0.1524" layer="91"/>
<junction x="111.76" y="147.32"/>
</segment>
</net>
<net name="GND" class="0">
<segment>
<pinref part="U$1" gate="G$1" pin="GND"/>
<wire x1="142.24" y1="109.22" x2="142.24" y2="111.76" width="0.1524" layer="91"/>
<wire x1="129.54" y1="111.76" x2="142.24" y2="111.76" width="0.1524" layer="91"/>
<pinref part="U1" gate="G$1" pin="GND"/>
<wire x1="129.54" y1="109.22" x2="129.54" y2="111.76" width="0.1524" layer="91"/>
</segment>
<segment>
<pinref part="C6" gate="G$1" pin="2"/>
<wire x1="101.6" y1="134.62" x2="101.6" y2="137.16" width="0.1524" layer="91"/>
<pinref part="U$7" gate="G$1" pin="GND"/>
</segment>
<segment>
<pinref part="R12" gate="G$1" pin="1"/>
<wire x1="111.76" y1="132.08" x2="111.76" y2="129.54" width="0.1524" layer="91"/>
<pinref part="U$8" gate="G$1" pin="GND"/>
</segment>
<segment>
<pinref part="C7" gate="G$1" pin="2"/>
<wire x1="132.08" y1="152.4" x2="132.08" y2="149.86" width="0.1524" layer="91"/>
<pinref part="U$9" gate="G$1" pin="GND"/>
</segment>
<segment>
<pinref part="R17" gate="G$1" pin="1"/>
<wire x1="193.04" y1="73.66" x2="193.04" y2="71.12" width="0.1524" layer="91"/>
<wire x1="193.04" y1="71.12" x2="200.66" y2="71.12" width="0.1524" layer="91"/>
<pinref part="R18" gate="G$1" pin="1"/>
<wire x1="200.66" y1="73.66" x2="200.66" y2="71.12" width="0.1524" layer="91"/>
<wire x1="200.66" y1="71.12" x2="200.66" y2="68.58" width="0.1524" layer="91"/>
<junction x="200.66" y="71.12"/>
<pinref part="U$26" gate="G$1" pin="GND"/>
</segment>
</net>
<net name="ECG-SW" class="0">
<segment>
<pinref part="U1" gate="G$1" pin="SW"/>
<pinref part="R13" gate="G$1" pin="2"/>
<wire x1="106.68" y1="48.26" x2="106.68" y2="60.96" width="0.1524" layer="91"/>
<wire x1="106.68" y1="60.96" x2="119.38" y2="60.96" width="0.1524" layer="91"/>
<wire x1="119.38" y1="60.96" x2="119.38" y2="63.5" width="0.1524" layer="91"/>
<label x="106.172" y="50.8" size="1.778" layer="95" rot="R90"/>
</segment>
</net>
<net name="ECG-FR" class="0">
<segment>
<pinref part="U1" gate="G$1" pin="FR"/>
<wire x1="147.32" y1="91.44" x2="193.04" y2="91.44" width="0.1524" layer="91"/>
<pinref part="R14" gate="G$1" pin="1"/>
<wire x1="193.04" y1="91.44" x2="193.04" y2="93.98" width="0.1524" layer="91"/>
<pinref part="R17" gate="G$1" pin="2"/>
<wire x1="193.04" y1="91.44" x2="193.04" y2="83.82" width="0.1524" layer="91"/>
<junction x="193.04" y="91.44"/>
<label x="149.86" y="91.694" size="1.778" layer="95"/>
</segment>
</net>
<net name="ECG-AC/!DC" class="0">
<segment>
<pinref part="U1" gate="G$1" pin="AC/!DC"/>
<wire x1="147.32" y1="88.9" x2="200.66" y2="88.9" width="0.1524" layer="91"/>
<pinref part="R15" gate="G$1" pin="1"/>
<wire x1="200.66" y1="88.9" x2="200.66" y2="93.98" width="0.1524" layer="91"/>
<pinref part="R18" gate="G$1" pin="2"/>
<wire x1="200.66" y1="88.9" x2="200.66" y2="83.82" width="0.1524" layer="91"/>
<junction x="200.66" y="88.9"/>
<label x="149.86" y="89.154" size="1.778" layer="95"/>
</segment>
</net>
<net name="ECG-!SDN" class="0">
<segment>
<pinref part="U1" gate="G$1" pin="!SDN"/>
<wire x1="147.32" y1="86.36" x2="167.64" y2="86.36" width="0.1524" layer="91"/>
<label x="149.86" y="86.614" size="1.778" layer="95"/>
<pinref part="U$2" gate="G$1" pin="IN"/>
</segment>
</net>
<net name="ECG-LOD_N" class="0">
<segment>
<pinref part="U1" gate="G$1" pin="LOD-"/>
<wire x1="147.32" y1="81.28" x2="167.64" y2="81.28" width="0.1524" layer="91"/>
<label x="149.86" y="81.534" size="1.778" layer="95"/>
<pinref part="U$39" gate="G$1" pin="OUT"/>
</segment>
</net>
<net name="3V3" class="0">
<segment>
<pinref part="U1" gate="G$1" pin="VS+"/>
<wire x1="127" y1="109.22" x2="127" y2="162.56" width="0.1524" layer="91"/>
<wire x1="127" y1="162.56" x2="132.08" y2="162.56" width="0.1524" layer="91"/>
<pinref part="C7" gate="G$1" pin="1"/>
<wire x1="132.08" y1="160.02" x2="132.08" y2="162.56" width="0.1524" layer="91"/>
<wire x1="132.08" y1="162.56" x2="132.08" y2="165.1" width="0.1524" layer="91"/>
<junction x="132.08" y="162.56"/>
<pinref part="U$11" gate="G$1" pin="V+"/>
<label x="132.08" y="167.894" size="1.778" layer="95" align="bottom-center"/>
<pinref part="R11" gate="G$1" pin="1"/>
<wire x1="111.76" y1="162.56" x2="111.76" y2="160.02" width="0.1524" layer="91"/>
<wire x1="127" y1="162.56" x2="111.76" y2="162.56" width="0.1524" layer="91"/>
<junction x="127" y="162.56"/>
</segment>
<segment>
<pinref part="R14" gate="G$1" pin="2"/>
<wire x1="193.04" y1="104.14" x2="193.04" y2="106.68" width="0.1524" layer="91"/>
<wire x1="193.04" y1="106.68" x2="200.66" y2="106.68" width="0.1524" layer="91"/>
<pinref part="R15" gate="G$1" pin="2"/>
<wire x1="200.66" y1="104.14" x2="200.66" y2="106.68" width="0.1524" layer="91"/>
<label x="200.66" y="112.014" size="1.778" layer="95" align="bottom-center"/>
<pinref part="U$12" gate="G$1" pin="V+"/>
<wire x1="200.66" y1="106.68" x2="200.66" y2="109.22" width="0.1524" layer="91"/>
<junction x="200.66" y="106.68"/>
</segment>
</net>
</nets>
</sheet>
<sheet>
<plain>
<text x="25.4" y="62.484" size="1.778" layer="97" rot="R270">DNP</text>
<text x="10.16" y="85.344" size="1.778" layer="97" rot="R270">DNP</text>
<text x="149.86" y="68.58" size="1.778" layer="97">Connect bridge wire
to use interrupt functionality</text>
<text x="99.06" y="88.9" size="5.08" layer="97" align="bottom-center">ADC</text>
<text x="137.16" y="154.94" size="5.08" layer="97" align="bottom-center">GPIO Expander</text>
<text x="223.52" y="78.74" size="5.08" layer="97" align="bottom-center">Connector</text>
<text x="59.944" y="7.62" size="1.778" layer="97" rot="R180">DNP</text>
</plain>
<instances>
<instance part="FRAME2" gate="G$1" x="0" y="0" smashed="yes">
<attribute name="DRAWING_NAME" x="217.17" y="15.24" size="2.54" layer="94"/>
<attribute name="LAST_DATE_TIME" x="217.17" y="10.16" size="2.286" layer="94"/>
<attribute name="SHEET" x="230.505" y="5.08" size="2.54" layer="94"/>
<attribute name="NOTE" x="163.83" y="20.32" size="2.286" layer="94"/>
<attribute name="SHEET_NAME" x="217.17" y="20.32" size="2.54" layer="94"/>
</instance>
<instance part="U2" gate="G$1" x="99.06" y="58.42" smashed="yes">
<attribute name="NAME" x="86.36" y="84.82" size="2.0828" layer="95" ratio="10" rot="SR0"/>
<attribute name="VALUE" x="86.36" y="29.02" size="2.0828" layer="96" ratio="10" rot="SR0"/>
</instance>
<instance part="R19" gate="G$1" x="12.7" y="78.74" smashed="yes" rot="R90">
<attribute name="NAME" x="11.2014" y="74.93" size="1.778" layer="95" rot="R90"/>
<attribute name="VALUE" x="16.002" y="74.93" size="1.778" layer="96" rot="R90"/>
</instance>
<instance part="R20" gate="G$1" x="20.32" y="60.96" smashed="yes" rot="R90">
<attribute name="NAME" x="18.8214" y="57.15" size="1.778" layer="95" rot="R90"/>
<attribute name="VALUE" x="23.622" y="57.15" size="1.778" layer="96" rot="R90"/>
</instance>
<instance part="R21" gate="G$1" x="20.32" y="78.74" smashed="yes" rot="R90">
<attribute name="NAME" x="18.8214" y="74.93" size="1.778" layer="95" rot="R90"/>
<attribute name="VALUE" x="23.622" y="74.93" size="1.778" layer="96" rot="R90"/>
</instance>
<instance part="R22" gate="G$1" x="12.7" y="60.96" smashed="yes" rot="R90">
<attribute name="NAME" x="11.2014" y="57.15" size="1.778" layer="95" rot="R90"/>
<attribute name="VALUE" x="16.002" y="57.15" size="1.778" layer="96" rot="R90"/>
</instance>
<instance part="U$10" gate="G$1" x="20.32" y="88.9" smashed="yes"/>
<instance part="U$13" gate="G$1" x="20.32" y="48.26" smashed="yes"/>
<instance part="U$14" gate="G$1" x="119.38" y="33.02" smashed="yes"/>
<instance part="C8" gate="G$1" x="142.24" y="86.36" smashed="yes">
<attribute name="NAME" x="143.764" y="86.741" size="1.778" layer="95"/>
<attribute name="VALUE" x="143.764" y="81.661" size="1.778" layer="96"/>
</instance>
<instance part="C9" gate="G$1" x="127" y="91.44" smashed="yes">
<attribute name="NAME" x="128.524" y="91.821" size="1.778" layer="95"/>
<attribute name="VALUE" x="128.524" y="86.741" size="1.778" layer="96"/>
</instance>
<instance part="U$15" gate="G$1" x="127" y="81.28" smashed="yes"/>
<instance part="U$16" gate="G$1" x="142.24" y="76.2" smashed="yes"/>
<instance part="U$17" gate="G$1" x="127" y="99.06" smashed="yes"/>
<instance part="U$18" gate="G$1" x="142.24" y="93.98" smashed="yes"/>
<instance part="R23" gate="G$1" x="127" y="71.12" smashed="yes" rot="R90">
<attribute name="NAME" x="125.5014" y="67.31" size="1.778" layer="95" rot="R90"/>
<attribute name="VALUE" x="130.302" y="67.31" size="1.778" layer="96" rot="R90"/>
</instance>
<instance part="U$21" gate="G$1" x="63.5" y="66.04" smashed="yes"/>
<instance part="U$19" gate="G$1" x="213.36" y="63.5" smashed="yes"/>
<instance part="U$20" gate="G$1" x="220.98" y="58.42" smashed="yes"/>
<instance part="JP1" gate="A" x="228.6" y="66.04" smashed="yes">
<attribute name="NAME" x="222.25" y="74.295" size="1.778" layer="95"/>
<attribute name="VALUE" x="222.25" y="58.42" size="1.778" layer="96"/>
</instance>
<instance part="U$24" gate="G$1" x="27.94" y="17.78" smashed="yes"/>
<instance part="U$3" gate="G$1" x="27.94" y="12.7" smashed="yes"/>
<instance part="U$4" gate="G$1" x="27.94" y="27.94" smashed="yes"/>
<instance part="U$25" gate="G$1" x="27.94" y="22.86" smashed="yes"/>
<instance part="U$28" gate="G$1" x="50.8" y="50.8" smashed="yes"/>
<instance part="U$29" gate="G$1" x="55.88" y="50.8" smashed="yes"/>
<instance part="U$23" gate="G$1" x="180.34" y="147.32" smashed="yes"/>
<instance part="U3" gate="G$1" x="127" y="139.7" smashed="yes">
<attribute name="NAME" x="127" y="150.114" size="1.778" layer="95" align="bottom-center"/>
<attribute name="VALUE" x="127" y="126.746" size="1.778" layer="96" align="top-center"/>
</instance>
<instance part="C10" gate="G$1" x="99.06" y="160.02" smashed="yes">
<attribute name="NAME" x="100.584" y="160.401" size="1.778" layer="95"/>
<attribute name="VALUE" x="100.584" y="155.321" size="1.778" layer="96"/>
</instance>
<instance part="R24" gate="G$1" x="91.44" y="152.4" smashed="yes" rot="R90">
<attribute name="NAME" x="89.9414" y="148.59" size="1.778" layer="95" rot="R90"/>
<attribute name="VALUE" x="94.742" y="148.59" size="1.778" layer="96" rot="R90"/>
</instance>
<instance part="R25" gate="G$1" x="83.82" y="152.4" smashed="yes" rot="R90">
<attribute name="NAME" x="82.3214" y="148.59" size="1.778" layer="95" rot="R90"/>
<attribute name="VALUE" x="87.122" y="148.59" size="1.778" layer="96" rot="R90"/>
</instance>
<instance part="R26" gate="G$1" x="76.2" y="152.4" smashed="yes" rot="R90">
<attribute name="NAME" x="74.7014" y="148.59" size="1.778" layer="95" rot="R90"/>
<attribute name="VALUE" x="79.502" y="148.59" size="1.778" layer="96" rot="R90"/>
</instance>
<instance part="R27" gate="G$1" x="91.44" y="121.92" smashed="yes" rot="R90">
<attribute name="NAME" x="89.9414" y="118.11" size="1.778" layer="95" rot="R90"/>
<attribute name="VALUE" x="94.742" y="118.11" size="1.778" layer="96" rot="R90"/>
</instance>
<instance part="R28" gate="G$1" x="83.82" y="121.92" smashed="yes" rot="R90">
<attribute name="NAME" x="82.3214" y="118.11" size="1.778" layer="95" rot="R90"/>
<attribute name="VALUE" x="87.122" y="118.11" size="1.778" layer="96" rot="R90"/>
</instance>
<instance part="R29" gate="G$1" x="76.2" y="121.92" smashed="yes" rot="R90">
<attribute name="NAME" x="74.7014" y="118.11" size="1.778" layer="95" rot="R90"/>
<attribute name="VALUE" x="79.502" y="118.11" size="1.778" layer="96" rot="R90"/>
</instance>
<instance part="U$27" gate="G$1" x="91.44" y="109.22" smashed="yes"/>
<instance part="U$30" gate="G$1" x="99.06" y="149.86" smashed="yes"/>
<instance part="U$31" gate="G$1" x="91.44" y="162.56" smashed="yes"/>
<instance part="U$32" gate="G$1" x="99.06" y="167.64" smashed="yes"/>
<instance part="TP1" gate="G$1" x="63.5" y="132.08" smashed="yes" rot="R90">
<attribute name="NAME" x="62.23" y="130.81" size="1.778" layer="95" rot="R90"/>
<attribute name="TP_SIGNAL_NAME" x="64.77" y="133.35" size="1.778" layer="97" rot="R90"/>
</instance>
<instance part="U$33" gate="G$1" x="109.22" y="124.46" smashed="yes"/>
<instance part="C11" gate="G$1" x="58.42" y="43.18" smashed="yes">
<attribute name="NAME" x="59.944" y="43.561" size="1.778" layer="95"/>
<attribute name="VALUE" x="59.944" y="38.481" size="1.778" layer="96"/>
</instance>
<instance part="U$34" gate="G$1" x="58.42" y="33.02" smashed="yes"/>
<instance part="U$22" gate="G$1" x="160.02" y="144.78" smashed="yes" rot="R180"/>
<instance part="TP4" gate="G$1" x="60.96" y="81.28" smashed="yes">
<attribute name="NAME" x="59.69" y="82.55" size="1.778" layer="95"/>
<attribute name="TP_SIGNAL_NAME" x="62.23" y="80.01" size="1.778" layer="97"/>
</instance>
<instance part="TP3" gate="G$1" x="144.78" y="68.58" smashed="yes">
<attribute name="NAME" x="143.51" y="69.85" size="1.778" layer="95"/>
<attribute name="TP_SIGNAL_NAME" x="146.05" y="67.31" size="1.778" layer="97"/>
</instance>
<instance part="R16" gate="G$1" x="68.58" y="152.4" smashed="yes" rot="R90">
<attribute name="NAME" x="67.0814" y="148.59" size="1.778" layer="95" rot="R90"/>
<attribute name="VALUE" x="71.882" y="148.59" size="1.778" layer="96" rot="R90"/>
</instance>
<instance part="U$35" gate="G$1" x="180.34" y="142.24" smashed="yes"/>
<instance part="U$36" gate="G$1" x="160.02" y="139.7" smashed="yes" rot="R180"/>
<instance part="R30" gate="G$1" x="167.64" y="154.94" smashed="yes" rot="R90">
<attribute name="NAME" x="166.1414" y="151.13" size="1.778" layer="95" rot="R90"/>
<attribute name="VALUE" x="170.942" y="151.13" size="1.778" layer="96" rot="R90"/>
</instance>
<instance part="R31" gate="G$1" x="175.26" y="154.94" smashed="yes" rot="R90">
<attribute name="NAME" x="173.7614" y="151.13" size="1.778" layer="95" rot="R90"/>
<attribute name="VALUE" x="178.562" y="151.13" size="1.778" layer="96" rot="R90"/>
</instance>
<instance part="U$37" gate="G$1" x="175.26" y="165.1" smashed="yes"/>
<instance part="R32" gate="G$1" x="48.26" y="27.94" smashed="yes">
<attribute name="NAME" x="44.45" y="29.4386" size="1.778" layer="95"/>
<attribute name="VALUE" x="44.45" y="24.638" size="1.778" layer="96"/>
</instance>
<instance part="R33" gate="G$1" x="48.26" y="17.78" smashed="yes">
<attribute name="NAME" x="44.45" y="19.2786" size="1.778" layer="95"/>
<attribute name="VALUE" x="44.45" y="14.478" size="1.778" layer="96"/>
</instance>
<instance part="R34" gate="G$1" x="58.42" y="22.86" smashed="yes">
<attribute name="NAME" x="54.61" y="24.3586" size="1.778" layer="95"/>
<attribute name="VALUE" x="54.61" y="19.558" size="1.778" layer="96"/>
</instance>
<instance part="R35" gate="G$1" x="58.42" y="12.7" smashed="yes">
<attribute name="NAME" x="54.61" y="14.1986" size="1.778" layer="95"/>
<attribute name="VALUE" x="54.61" y="9.398" size="1.778" layer="96"/>
</instance>
<instance part="R36" gate="G$1" x="193.04" y="124.46" smashed="yes" rot="R90">
<attribute name="NAME" x="191.5414" y="120.65" size="1.778" layer="95" rot="R90"/>
<attribute name="VALUE" x="196.342" y="120.65" size="1.778" layer="96" rot="R90"/>
</instance>
<instance part="D1" gate="G$1" x="193.04" y="111.76" smashed="yes">
<attribute name="NAME" x="196.596" y="107.188" size="1.778" layer="95" rot="R90"/>
<attribute name="VALUE" x="198.755" y="107.188" size="1.778" layer="96" rot="R90"/>
</instance>
<instance part="U$38" gate="G$1" x="193.04" y="101.6" smashed="yes"/>
<instance part="U$40" gate="G$1" x="160.02" y="129.54" smashed="yes" rot="R180"/>
</instances>
<busses>
</busses>
<nets>
<net name="ADC-A1" class="0">
<segment>
<pinref part="U2" gate="G$1" pin="A1"/>
<wire x1="81.28" y1="68.58" x2="20.32" y2="68.58" width="0.1524" layer="91"/>
<pinref part="R20" gate="G$1" pin="2"/>
<wire x1="20.32" y1="68.58" x2="20.32" y2="66.04" width="0.1524" layer="91"/>
<pinref part="R21" gate="G$1" pin="1"/>
<wire x1="20.32" y1="68.58" x2="20.32" y2="73.66" width="0.1524" layer="91"/>
<junction x="20.32" y="68.58"/>
<label x="53.34" y="68.834" size="1.778" layer="95"/>
</segment>
</net>
<net name="ADC-A0" class="0">
<segment>
<pinref part="U2" gate="G$1" pin="A0"/>
<wire x1="81.28" y1="71.12" x2="12.7" y2="71.12" width="0.1524" layer="91"/>
<pinref part="R22" gate="G$1" pin="2"/>
<pinref part="R19" gate="G$1" pin="1"/>
<wire x1="12.7" y1="66.04" x2="12.7" y2="71.12" width="0.1524" layer="91"/>
<wire x1="12.7" y1="71.12" x2="12.7" y2="73.66" width="0.1524" layer="91"/>
<junction x="12.7" y="71.12"/>
<label x="53.34" y="71.374" size="1.778" layer="95"/>
</segment>
</net>
<net name="GND" class="0">
<segment>
<pinref part="R20" gate="G$1" pin="1"/>
<wire x1="20.32" y1="55.88" x2="20.32" y2="53.34" width="0.1524" layer="91"/>
<wire x1="20.32" y1="53.34" x2="12.7" y2="53.34" width="0.1524" layer="91"/>
<pinref part="R22" gate="G$1" pin="1"/>
<wire x1="12.7" y1="53.34" x2="12.7" y2="55.88" width="0.1524" layer="91"/>
<wire x1="20.32" y1="53.34" x2="20.32" y2="50.8" width="0.1524" layer="91"/>
<junction x="20.32" y="53.34"/>
<pinref part="U$13" gate="G$1" pin="GND"/>
</segment>
<segment>
<pinref part="U2" gate="G$1" pin="DGND"/>
<wire x1="116.84" y1="38.1" x2="119.38" y2="38.1" width="0.1524" layer="91"/>
<wire x1="119.38" y1="38.1" x2="119.38" y2="40.64" width="0.1524" layer="91"/>
<pinref part="U2" gate="G$1" pin="AGND"/>
<wire x1="119.38" y1="40.64" x2="116.84" y2="40.64" width="0.1524" layer="91"/>
<wire x1="119.38" y1="38.1" x2="119.38" y2="35.56" width="0.1524" layer="91"/>
<junction x="119.38" y="38.1"/>
<pinref part="U$14" gate="G$1" pin="GND"/>
</segment>
<segment>
<pinref part="C9" gate="G$1" pin="2"/>
<pinref part="U$15" gate="G$1" pin="GND"/>
<wire x1="127" y1="86.36" x2="127" y2="83.82" width="0.1524" layer="91"/>
</segment>
<segment>
<pinref part="C8" gate="G$1" pin="2"/>
<wire x1="142.24" y1="81.28" x2="142.24" y2="78.74" width="0.1524" layer="91"/>
<pinref part="U$16" gate="G$1" pin="GND"/>
</segment>
<segment>
<wire x1="220.98" y1="63.5" x2="220.98" y2="60.96" width="0.1524" layer="91"/>
<pinref part="U$20" gate="G$1" pin="GND"/>
<wire x1="220.98" y1="63.5" x2="226.06" y2="63.5" width="0.1524" layer="91"/>
<pinref part="JP1" gate="A" pin="4"/>
</segment>
<segment>
<pinref part="U2" gate="G$1" pin="REFN"/>
<wire x1="81.28" y1="55.88" x2="50.8" y2="55.88" width="0.1524" layer="91"/>
<wire x1="50.8" y1="55.88" x2="50.8" y2="53.34" width="0.1524" layer="91"/>
<pinref part="U$28" gate="G$1" pin="GND"/>
</segment>
<segment>
<pinref part="R29" gate="G$1" pin="1"/>
<wire x1="76.2" y1="116.84" x2="76.2" y2="114.3" width="0.1524" layer="91"/>
<wire x1="76.2" y1="114.3" x2="83.82" y2="114.3" width="0.1524" layer="91"/>
<pinref part="R27" gate="G$1" pin="1"/>
<wire x1="83.82" y1="114.3" x2="91.44" y2="114.3" width="0.1524" layer="91"/>
<wire x1="91.44" y1="114.3" x2="91.44" y2="116.84" width="0.1524" layer="91"/>
<pinref part="R28" gate="G$1" pin="1"/>
<wire x1="83.82" y1="116.84" x2="83.82" y2="114.3" width="0.1524" layer="91"/>
<junction x="83.82" y="114.3"/>
<wire x1="91.44" y1="114.3" x2="91.44" y2="111.76" width="0.1524" layer="91"/>
<junction x="91.44" y="114.3"/>
<pinref part="U$27" gate="G$1" pin="GND"/>
</segment>
<segment>
<pinref part="C10" gate="G$1" pin="2"/>
<wire x1="99.06" y1="154.94" x2="99.06" y2="152.4" width="0.1524" layer="91"/>
<pinref part="U$30" gate="G$1" pin="GND"/>
</segment>
<segment>
<pinref part="U3" gate="G$1" pin="VSS"/>
<wire x1="111.76" y1="129.54" x2="109.22" y2="129.54" width="0.1524" layer="91"/>
<wire x1="109.22" y1="129.54" x2="109.22" y2="127" width="0.1524" layer="91"/>
<pinref part="U$33" gate="G$1" pin="GND"/>
</segment>
<segment>
<pinref part="C11" gate="G$1" pin="2"/>
<wire x1="58.42" y1="38.1" x2="58.42" y2="35.56" width="0.1524" layer="91"/>
<pinref part="U$34" gate="G$1" pin="GND"/>
</segment>
<segment>
<pinref part="D1" gate="G$1" pin="C"/>
<wire x1="193.04" y1="106.68" x2="193.04" y2="104.14" width="0.1524" layer="91"/>
<pinref part="U$38" gate="G$1" pin="GND"/>
</segment>
</net>
<net name="3V3" class="0">
<segment>
<pinref part="U2" gate="G$1" pin="AVDD"/>
<wire x1="116.84" y1="81.28" x2="121.92" y2="81.28" width="0.1524" layer="91"/>
<wire x1="121.92" y1="81.28" x2="121.92" y2="96.52" width="0.1524" layer="91"/>
<wire x1="121.92" y1="96.52" x2="127" y2="96.52" width="0.1524" layer="91"/>
<pinref part="C9" gate="G$1" pin="1"/>
<wire x1="127" y1="96.52" x2="127" y2="93.98" width="0.1524" layer="91"/>
<wire x1="127" y1="96.52" x2="127" y2="99.06" width="0.1524" layer="91"/>
<junction x="127" y="96.52"/>
<pinref part="U$17" gate="G$1" pin="V+"/>
<label x="127" y="101.854" size="1.778" layer="95" align="bottom-center"/>
</segment>
<segment>
<pinref part="U2" gate="G$1" pin="DVDD"/>
<wire x1="116.84" y1="78.74" x2="127" y2="78.74" width="0.1524" layer="91"/>
<wire x1="127" y1="78.74" x2="137.16" y2="78.74" width="0.1524" layer="91"/>
<wire x1="137.16" y1="78.74" x2="137.16" y2="91.44" width="0.1524" layer="91"/>
<wire x1="137.16" y1="91.44" x2="142.24" y2="91.44" width="0.1524" layer="91"/>
<pinref part="C8" gate="G$1" pin="1"/>
<wire x1="142.24" y1="91.44" x2="142.24" y2="88.9" width="0.1524" layer="91"/>
<wire x1="142.24" y1="91.44" x2="142.24" y2="93.98" width="0.1524" layer="91"/>
<junction x="142.24" y="91.44"/>
<pinref part="U$18" gate="G$1" pin="V+"/>
<label x="142.24" y="96.774" size="1.778" layer="95" align="bottom-center"/>
<pinref part="R23" gate="G$1" pin="2"/>
<wire x1="127" y1="76.2" x2="127" y2="78.74" width="0.1524" layer="91"/>
<junction x="127" y="78.74"/>
</segment>
<segment>
<wire x1="213.36" y1="60.96" x2="213.36" y2="63.5" width="0.1524" layer="91"/>
<pinref part="U$19" gate="G$1" pin="V+"/>
<label x="213.36" y="66.294" size="1.778" layer="95" align="bottom-center"/>
<wire x1="213.36" y1="60.96" x2="218.44" y2="60.96" width="0.1524" layer="91"/>
<wire x1="218.44" y1="60.96" x2="218.44" y2="66.04" width="0.1524" layer="91"/>
<wire x1="218.44" y1="66.04" x2="226.06" y2="66.04" width="0.1524" layer="91"/>
<pinref part="JP1" gate="A" pin="3"/>
</segment>
<segment>
<pinref part="U2" gate="G$1" pin="REFP"/>
<wire x1="81.28" y1="53.34" x2="58.42" y2="53.34" width="0.1524" layer="91"/>
<wire x1="58.42" y1="53.34" x2="58.42" y2="48.26" width="0.1524" layer="91"/>
<wire x1="58.42" y1="48.26" x2="55.88" y2="48.26" width="0.1524" layer="91"/>
<wire x1="55.88" y1="48.26" x2="55.88" y2="50.8" width="0.1524" layer="91"/>
<pinref part="U$29" gate="G$1" pin="V+"/>
<label x="55.88" y="53.594" size="1.778" layer="95" align="bottom-center"/>
<pinref part="C11" gate="G$1" pin="1"/>
<wire x1="58.42" y1="45.72" x2="58.42" y2="48.26" width="0.1524" layer="91"/>
<junction x="58.42" y="48.26"/>
</segment>
<segment>
<pinref part="R21" gate="G$1" pin="2"/>
<wire x1="20.32" y1="83.82" x2="20.32" y2="86.36" width="0.1524" layer="91"/>
<wire x1="20.32" y1="86.36" x2="12.7" y2="86.36" width="0.1524" layer="91"/>
<pinref part="R19" gate="G$1" pin="2"/>
<wire x1="12.7" y1="86.36" x2="12.7" y2="83.82" width="0.1524" layer="91"/>
<wire x1="20.32" y1="86.36" x2="20.32" y2="88.9" width="0.1524" layer="91"/>
<junction x="20.32" y="86.36"/>
<pinref part="U$10" gate="G$1" pin="V+"/>
<label x="20.32" y="91.694" size="1.778" layer="95" align="bottom-center"/>
</segment>
<segment>
<pinref part="U3" gate="G$1" pin="VDD"/>
<wire x1="111.76" y1="147.32" x2="109.22" y2="147.32" width="0.1524" layer="91"/>
<wire x1="109.22" y1="147.32" x2="109.22" y2="165.1" width="0.1524" layer="91"/>
<wire x1="109.22" y1="165.1" x2="99.06" y2="165.1" width="0.1524" layer="91"/>
<pinref part="C10" gate="G$1" pin="1"/>
<wire x1="99.06" y1="165.1" x2="99.06" y2="162.56" width="0.1524" layer="91"/>
<wire x1="99.06" y1="165.1" x2="99.06" y2="167.64" width="0.1524" layer="91"/>
<junction x="99.06" y="165.1"/>
<pinref part="U$32" gate="G$1" pin="V+"/>
<label x="99.06" y="170.434" size="1.778" layer="95" align="bottom-center"/>
</segment>
<segment>
<pinref part="R24" gate="G$1" pin="2"/>
<wire x1="91.44" y1="157.48" x2="91.44" y2="160.02" width="0.1524" layer="91"/>
<pinref part="R26" gate="G$1" pin="2"/>
<wire x1="91.44" y1="160.02" x2="83.82" y2="160.02" width="0.1524" layer="91"/>
<wire x1="83.82" y1="160.02" x2="76.2" y2="160.02" width="0.1524" layer="91"/>
<wire x1="76.2" y1="160.02" x2="76.2" y2="157.48" width="0.1524" layer="91"/>
<pinref part="R25" gate="G$1" pin="2"/>
<wire x1="83.82" y1="157.48" x2="83.82" y2="160.02" width="0.1524" layer="91"/>
<junction x="83.82" y="160.02"/>
<wire x1="91.44" y1="160.02" x2="91.44" y2="162.56" width="0.1524" layer="91"/>
<junction x="91.44" y="160.02"/>
<pinref part="U$31" gate="G$1" pin="V+"/>
<label x="91.44" y="165.354" size="1.778" layer="95" align="bottom-center"/>
<wire x1="76.2" y1="160.02" x2="68.58" y2="160.02" width="0.1524" layer="91"/>
<junction x="76.2" y="160.02"/>
<pinref part="R16" gate="G$1" pin="2"/>
<wire x1="68.58" y1="160.02" x2="68.58" y2="157.48" width="0.1524" layer="91"/>
</segment>
<segment>
<pinref part="R30" gate="G$1" pin="2"/>
<wire x1="167.64" y1="160.02" x2="167.64" y2="162.56" width="0.1524" layer="91"/>
<wire x1="167.64" y1="162.56" x2="175.26" y2="162.56" width="0.1524" layer="91"/>
<pinref part="R31" gate="G$1" pin="2"/>
<wire x1="175.26" y1="162.56" x2="175.26" y2="160.02" width="0.1524" layer="91"/>
<wire x1="175.26" y1="162.56" x2="175.26" y2="165.1" width="0.1524" layer="91"/>
<junction x="175.26" y="162.56"/>
<pinref part="U$37" gate="G$1" pin="V+"/>
<label x="175.26" y="167.894" size="1.778" layer="95" align="bottom-center"/>
</segment>
</net>
<net name="ECG-SCL" class="0">
<segment>
<pinref part="U2" gate="G$1" pin="SCL"/>
<wire x1="81.28" y1="50.8" x2="63.5" y2="50.8" width="0.1524" layer="91"/>
<label x="66.04" y="51.054" size="1.778" layer="95"/>
</segment>
<segment>
<wire x1="226.06" y1="71.12" x2="198.12" y2="71.12" width="0.1524" layer="91"/>
<label x="200.66" y="71.374" size="1.778" layer="95"/>
<pinref part="JP1" gate="A" pin="1"/>
</segment>
<segment>
<pinref part="U3" gate="G$1" pin="SCL"/>
<wire x1="111.76" y1="137.16" x2="96.52" y2="137.16" width="0.1524" layer="91"/>
<label x="99.06" y="137.414" size="1.778" layer="95"/>
</segment>
</net>
<net name="ECG-SDA" class="0">
<segment>
<pinref part="U2" gate="G$1" pin="SDA"/>
<wire x1="81.28" y1="45.72" x2="63.5" y2="45.72" width="0.1524" layer="91"/>
<label x="66.04" y="45.974" size="1.778" layer="95"/>
</segment>
<segment>
<wire x1="226.06" y1="68.58" x2="198.12" y2="68.58" width="0.1524" layer="91"/>
<label x="200.66" y="68.834" size="1.778" layer="95"/>
<pinref part="JP1" gate="A" pin="2"/>
</segment>
<segment>
<pinref part="U3" gate="G$1" pin="SDA"/>
<wire x1="111.76" y1="134.62" x2="96.52" y2="134.62" width="0.1524" layer="91"/>
<label x="99.06" y="134.874" size="1.778" layer="95"/>
</segment>
</net>
<net name="ECG-!DRDY" class="0">
<segment>
<pinref part="U2" gate="G$1" pin="!DRDY"/>
<wire x1="116.84" y1="73.66" x2="119.38" y2="73.66" width="0.1524" layer="91"/>
<wire x1="119.38" y1="73.66" x2="119.38" y2="63.5" width="0.1524" layer="91"/>
<wire x1="119.38" y1="63.5" x2="127" y2="63.5" width="0.1524" layer="91"/>
<pinref part="R23" gate="G$1" pin="1"/>
<wire x1="127" y1="63.5" x2="144.78" y2="63.5" width="0.1524" layer="91"/>
<wire x1="127" y1="66.04" x2="127" y2="63.5" width="0.1524" layer="91"/>
<junction x="127" y="63.5"/>
<label x="129.54" y="63.754" size="1.778" layer="95"/>
<pinref part="TP3" gate="G$1" pin="TP"/>
<wire x1="144.78" y1="66.04" x2="144.78" y2="63.5" width="0.1524" layer="91"/>
<wire x1="144.78" y1="63.5" x2="147.32" y2="63.5" width="0.1524" layer="91"/>
<junction x="144.78" y="63.5"/>
</segment>
<segment>
<wire x1="142.24" y1="139.7" x2="160.02" y2="139.7" width="0.1524" layer="91"/>
<label x="144.78" y="139.954" size="1.778" layer="95"/>
<pinref part="U3" gate="G$1" pin="P3"/>
<pinref part="U$36" gate="G$1" pin="IN"/>
</segment>
</net>
<net name="ECG-OUT" class="0">
<segment>
<pinref part="U2" gate="G$1" pin="AIN0"/>
<wire x1="81.28" y1="66.04" x2="63.5" y2="66.04" width="0.1524" layer="91"/>
<pinref part="U$21" gate="G$1" pin="IN"/>
<label x="66.04" y="66.294" size="1.778" layer="95"/>
</segment>
</net>
<net name="ECG-LOD_P" class="0">
<segment>
<pinref part="U3" gate="G$1" pin="P1"/>
<wire x1="142.24" y1="144.78" x2="160.02" y2="144.78" width="0.1524" layer="91"/>
<label x="144.78" y="145.034" size="1.778" layer="95"/>
<pinref part="U$22" gate="G$1" pin="IN"/>
</segment>
</net>
<net name="ADC-!RESET" class="0">
<segment>
<pinref part="U2" gate="G$1" pin="!RESET"/>
<label x="63.5" y="76.454" size="1.778" layer="95"/>
<wire x1="60.96" y1="76.2" x2="78.74" y2="76.2" width="0.1524" layer="91"/>
<wire x1="78.74" y1="76.2" x2="78.74" y2="73.66" width="0.1524" layer="91"/>
<wire x1="78.74" y1="73.66" x2="81.28" y2="73.66" width="0.1524" layer="91"/>
<pinref part="TP4" gate="G$1" pin="TP"/>
<wire x1="60.96" y1="78.74" x2="60.96" y2="76.2" width="0.1524" layer="91"/>
<wire x1="60.96" y1="76.2" x2="58.42" y2="76.2" width="0.1524" layer="91"/>
<junction x="60.96" y="76.2"/>
</segment>
<segment>
<pinref part="U3" gate="G$1" pin="P2"/>
<wire x1="142.24" y1="142.24" x2="167.64" y2="142.24" width="0.1524" layer="91"/>
<label x="144.78" y="142.494" size="1.778" layer="95"/>
<pinref part="U$35" gate="G$1" pin="OUT"/>
<pinref part="R30" gate="G$1" pin="1"/>
<wire x1="167.64" y1="142.24" x2="180.34" y2="142.24" width="0.1524" layer="91"/>
<wire x1="167.64" y1="149.86" x2="167.64" y2="142.24" width="0.1524" layer="91"/>
<junction x="167.64" y="142.24"/>
</segment>
</net>
<net name="ECG-IAOUT" class="0">
<segment>
<wire x1="43.18" y1="17.78" x2="27.94" y2="17.78" width="0.1524" layer="91"/>
<pinref part="U$24" gate="G$1" pin="IN"/>
<label x="30.48" y="18.034" size="1.778" layer="95"/>
<pinref part="R33" gate="G$1" pin="1"/>
</segment>
</net>
<net name="ECG-RLD" class="0">
<segment>
<pinref part="U$3" gate="G$1" pin="IN"/>
<wire x1="27.94" y1="12.7" x2="53.34" y2="12.7" width="0.1524" layer="91"/>
<label x="30.48" y="12.954" size="1.778" layer="95"/>
<pinref part="R35" gate="G$1" pin="1"/>
</segment>
</net>
<net name="ECG-IN_P" class="0">
<segment>
<pinref part="U$4" gate="G$1" pin="IN"/>
<wire x1="27.94" y1="27.94" x2="43.18" y2="27.94" width="0.1524" layer="91"/>
<label x="30.48" y="28.194" size="1.778" layer="95"/>
<pinref part="R32" gate="G$1" pin="1"/>
</segment>
</net>
<net name="ECG-IN_N" class="0">
<segment>
<pinref part="U$25" gate="G$1" pin="IN"/>
<wire x1="27.94" y1="22.86" x2="53.34" y2="22.86" width="0.1524" layer="91"/>
<label x="30.48" y="23.114" size="1.778" layer="95"/>
<pinref part="R34" gate="G$1" pin="1"/>
</segment>
</net>
<net name="ECG-!SDN" class="0">
<segment>
<pinref part="U3" gate="G$1" pin="P0"/>
<wire x1="142.24" y1="147.32" x2="175.26" y2="147.32" width="0.1524" layer="91"/>
<label x="144.78" y="147.574" size="1.778" layer="95"/>
<pinref part="U$23" gate="G$1" pin="OUT"/>
<pinref part="R31" gate="G$1" pin="1"/>
<wire x1="175.26" y1="147.32" x2="180.34" y2="147.32" width="0.1524" layer="91"/>
<wire x1="175.26" y1="149.86" x2="175.26" y2="147.32" width="0.1524" layer="91"/>
<junction x="175.26" y="147.32"/>
</segment>
</net>
<net name="GPIO-A0" class="0">
<segment>
<pinref part="R24" gate="G$1" pin="1"/>
<pinref part="R27" gate="G$1" pin="2"/>
<wire x1="91.44" y1="147.32" x2="91.44" y2="144.78" width="0.1524" layer="91"/>
<pinref part="U3" gate="G$1" pin="A0"/>
<wire x1="91.44" y1="144.78" x2="91.44" y2="127" width="0.1524" layer="91"/>
<wire x1="111.76" y1="144.78" x2="91.44" y2="144.78" width="0.1524" layer="91"/>
<junction x="91.44" y="144.78"/>
<label x="99.06" y="145.034" size="1.778" layer="95"/>
</segment>
</net>
<net name="GPIO-A1" class="0">
<segment>
<pinref part="R25" gate="G$1" pin="1"/>
<pinref part="R28" gate="G$1" pin="2"/>
<wire x1="83.82" y1="147.32" x2="83.82" y2="142.24" width="0.1524" layer="91"/>
<pinref part="U3" gate="G$1" pin="A1"/>
<wire x1="83.82" y1="142.24" x2="83.82" y2="127" width="0.1524" layer="91"/>
<wire x1="111.76" y1="142.24" x2="83.82" y2="142.24" width="0.1524" layer="91"/>
<junction x="83.82" y="142.24"/>
<label x="99.06" y="142.494" size="1.778" layer="95"/>
</segment>
</net>
<net name="GPIO-A2" class="0">
<segment>
<pinref part="R26" gate="G$1" pin="1"/>
<pinref part="R29" gate="G$1" pin="2"/>
<wire x1="76.2" y1="147.32" x2="76.2" y2="139.7" width="0.1524" layer="91"/>
<pinref part="U3" gate="G$1" pin="A2"/>
<wire x1="76.2" y1="139.7" x2="76.2" y2="127" width="0.1524" layer="91"/>
<wire x1="111.76" y1="139.7" x2="76.2" y2="139.7" width="0.1524" layer="91"/>
<junction x="76.2" y="139.7"/>
<label x="99.06" y="139.954" size="1.778" layer="95"/>
</segment>
</net>
<net name="GPIO-!INT" class="0">
<segment>
<pinref part="U3" gate="G$1" pin="!INT"/>
<label x="99.06" y="132.334" size="1.778" layer="95"/>
<wire x1="111.76" y1="132.08" x2="68.58" y2="132.08" width="0.1524" layer="91"/>
<pinref part="R16" gate="G$1" pin="1"/>
<wire x1="68.58" y1="132.08" x2="68.58" y2="147.32" width="0.1524" layer="91"/>
<pinref part="TP1" gate="G$1" pin="TP"/>
<wire x1="68.58" y1="132.08" x2="66.04" y2="132.08" width="0.1524" layer="91"/>
<junction x="68.58" y="132.08"/>
</segment>
</net>
<net name="ADC-1" class="0">
<segment>
<pinref part="R32" gate="G$1" pin="2"/>
<wire x1="53.34" y1="27.94" x2="78.74" y2="27.94" width="0.1524" layer="91"/>
<label x="68.58" y="28.194" size="1.778" layer="95"/>
</segment>
<segment>
<wire x1="81.28" y1="58.42" x2="63.5" y2="58.42" width="0.1524" layer="91"/>
<label x="66.04" y="58.674" size="1.778" layer="95"/>
<pinref part="U2" gate="G$1" pin="AIN3"/>
</segment>
</net>
<net name="ADC-2" class="0">
<segment>
<pinref part="R34" gate="G$1" pin="2"/>
<wire x1="63.5" y1="22.86" x2="78.74" y2="22.86" width="0.1524" layer="91"/>
<label x="68.58" y="23.114" size="1.778" layer="95"/>
</segment>
<segment>
<wire x1="81.28" y1="60.96" x2="63.5" y2="60.96" width="0.1524" layer="91"/>
<label x="66.04" y="61.214" size="1.778" layer="95"/>
<pinref part="U2" gate="G$1" pin="AIN2"/>
</segment>
</net>
<net name="ADC-3" class="0">
<segment>
<pinref part="R33" gate="G$1" pin="2"/>
<wire x1="53.34" y1="17.78" x2="66.04" y2="17.78" width="0.1524" layer="91"/>
<pinref part="R35" gate="G$1" pin="2"/>
<wire x1="63.5" y1="12.7" x2="66.04" y2="12.7" width="0.1524" layer="91"/>
<wire x1="66.04" y1="12.7" x2="66.04" y2="17.78" width="0.1524" layer="91"/>
<junction x="66.04" y="17.78"/>
<wire x1="66.04" y1="17.78" x2="78.74" y2="17.78" width="0.1524" layer="91"/>
<label x="68.58" y="18.034" size="1.778" layer="95"/>
</segment>
<segment>
<wire x1="81.28" y1="63.5" x2="63.5" y2="63.5" width="0.1524" layer="91"/>
<label x="66.04" y="63.754" size="1.778" layer="95"/>
<pinref part="U2" gate="G$1" pin="AIN1"/>
</segment>
</net>
<net name="ECG-LED" class="0">
<segment>
<wire x1="193.04" y1="132.08" x2="193.04" y2="129.54" width="0.1524" layer="91"/>
<pinref part="R36" gate="G$1" pin="2"/>
<label x="144.78" y="132.334" size="1.778" layer="95"/>
<pinref part="U3" gate="G$1" pin="P6"/>
<wire x1="193.04" y1="132.08" x2="142.24" y2="132.08" width="0.1524" layer="91"/>
</segment>
</net>
<net name="ECG-LED-PD" class="0">
<segment>
<pinref part="D1" gate="G$1" pin="A"/>
<pinref part="R36" gate="G$1" pin="1"/>
<wire x1="193.04" y1="114.3" x2="193.04" y2="119.38" width="0.1524" layer="91"/>
<label x="193.04" y="116.84" size="1.778" layer="95"/>
</segment>
</net>
<net name="ECG-LOD_N" class="0">
<segment>
<pinref part="U3" gate="G$1" pin="P7"/>
<wire x1="142.24" y1="129.54" x2="160.02" y2="129.54" width="0.1524" layer="91"/>
<pinref part="U$40" gate="G$1" pin="IN"/>
<label x="144.78" y="129.794" size="1.778" layer="95"/>
</segment>
</net>
</nets>
</sheet>
</sheets>
</schematic>
</drawing>
<compatibility>
<note version="6.3" minversion="6.2.2" severity="warning">
Since Version 6.2.2 text objects can contain more than one line,
which will not be processed correctly with this version.
</note>
<note version="8.2" severity="warning">
Since Version 8.2, EAGLE supports online libraries. The ids
of those online libraries will not be understood (or retained)
with this version.
</note>
<note version="8.3" severity="warning">
Since Version 8.3, EAGLE supports URNs for individual library
assets (packages, symbols, and devices). The URNs of those assets
will not be understood (or retained) with this version.
</note>
<note version="8.3" severity="warning">
Since Version 8.3, EAGLE supports the association of 3D packages
with devices in libraries, schematics, and board files. Those 3D
packages will not be understood (or retained) with this version.
</note>
<note version="9.0" severity="warning">
Since Version 9.0, EAGLE supports the align property for labels. 
Labels in schematic will not be understood with this version. Update EAGLE to the latest version 
for full support of labels. 
</note>
</compatibility>
</eagle>
