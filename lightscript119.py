	
#bpy.app.debug = True
	
# ***** BEGIN GPL LICENSE BLOCK ***** 
# 
# This program is free software; you can redistribute it and/or 
# modify it under the terms of the GNU General Public License 
# as published by the Free Software Foundation; either version 2 
# of the License, or (at your option) any later version. 
# 
# This program is distributed in the hope that it will be useful, 
# but WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
# GNU General Public License for more details. 
# 
# You should have received a copy of the GNU General Public License 
# along with this program; if not, write to the Free Software Foundation, 
# Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA. 
# 
# ***** END GPL LICENCE BLOCK ***** 
#
#
# -------------------------------------------------------------------------------------------------------
# Blender 2.5 original Original script contact info:
# -------------------------------------------------------------------------------------------------------
# Creator of the script
# For questions/feature requests / Suggestions, contact Etoven at BlenderArtists.org
#
# Script created  by Etoven on the 14 January 2010
#  Script with no panel to set parameter
#  Only 3 points spots lamp and area light set up
#
#  Domain box   constraint added  lamp power  function of distance
#
#
#
#
#
# -------------------------------------------------
#
#
# -------------------------------------------------
# Blender 2.5 Modifications / additions:
# ------------------------------------------------
# 
# Contributors: Rickyblender  
# 
# url: http://blenderartists.org/forum/showthread.php?t=206986&p=1780008#post1780008
# 
#
# Script modified by Rickyblender on the 15 January 2010
# Added tool pro panel and menus and other properties as parameters 
# and added Studio and Day light scene light set up
#
#  Nodes set up for Sepia render
#  Sky box / Fake GI sky box  / Light Box / Fluo  Fixtures models
#  Day/night light and World set up 
#
# Implemented the New multi level menu 
#
# ---------------------------------------------------
#
# Drago2010uk has also help to modify and inprove the script in general
# Clay render
# Added in Feb a new menu set up with multi level
#
# 
#
# ----------------------------------------------------
#
# Also thanks for tips from Zeffi for World set up paremters  and  NRK for simple clouds
#
# 
# ----------------------------------------------------
#
# Rickyblender on 15 Fev 2012
# added new special render  Addsketchup1operator1
# 
#
# ---------------------------------------------------
#
# References
#
# noob to pro
# sky box
# http://en.wikibooks.org/wiki/Blender_3D:_Noob_to_Pro/Build_a_skybox
#
# Scripting
# http://en.wikibooks.org/wiki/Blender_3D:_Noob_to_Pro/Advanced_Tutorials/Python_Scripting/Introduction_New
#
# DOF
# http://www.yafaray.org/documentation/tutorials/dof
#
# Clay render
# http://www.yafaray.org/documentation/tutorials/clayrender
#
#
#  Spherical Sky dome
#
# http://wiki.blender.org/index.php/Doc:Manual/World/Background
#
#
# ---------------------------------------------------
#
#
#
# Warnings:
#
# First always save your file under a new name before using this script.
#
# This script will reset the world scene set up  to the default manufacturer'a scene and erase all lamps in the scene then it 
# will apply the selected light set up.
# So you will loose your scene world values set up  and lamps set up in you file.
#
#
# Viewport Start end end Clipping
#
# We also set at the begining of the script values for the viewport
#
# bpy.types.SpaceView3D.clip_start=0.1
# bpy.types.SpaceView3D.clip_end = 5000
#
# So you may have to manually change theses values if your scene has larger values after running the script!
#
#
#
# TODO: 
#
#
# --------------------------------------------------------------
# ADDON INFO THAT SHOWS IN USER PREFERENCES ADD-ONS
# --------------------------------------------------------------
	
	
	
bl_info = {
	"name": "Lighting Wizard",
	"description": "Sets up Scene Lighting",
	"author": "Etoven/Rickyblender/Dragon2010UK",
	"version": (1, 0),
	"blender": (2, 8, 0),
	"api": 35865,
	"location": "Tools Panel",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "",
	"category": "Scene Lighting"}
	
import bpy, math

from bpy.props import *
from math import *  
from decimal import *
from bpy_extras.object_utils import object_data_add
from bpy_extras.object_utils import AddObjectHelper	
from mathutils import Vector
	
menu_options = "None"
menu_choice = "None"
menu_one_point = "None"
menu_two_point = "None" 
menu_three_point = "None"
menu_four_point = "None"
	
menu_outdoor = "None"
menu_world="None"
skydome_menu="None"
menu_AO="None"
menu_Fluo="None"
menu_gen="None"
	
menu_special="None"
menu_other="None"
	
menu_angmap1="None"
	
energymult = .600
	
layers = [False]*20
layers[0] = True

s_padding = 1 				# Scene padding in blender units

minx = 0
miny = 0
minz = 0
	
maxx = 0
maxy = 0
maxz = 0
	
lightboxtype=False
	
bpy.types.Scene.Ckeckskydomebright1 = BoolProperty(
	name="Wings", 
	description="True or False?")
	
bpy.types.Scene.skydomeradius = FloatProperty(							#  Myfloat is the name of the Float variable = Scene property
	name="Sky Dome Radius",												#  Name printed in button
	description="Enter Sky Dome Radius",								#  Tip tool
	default = 12.0,
	min = 0.0,
	max = 100)
	
# Define max min for viewport  
bpy.types.SpaceView3D.clip_start=0.1
bpy.types.SpaceView3D.clip_end = 5000
	
print ('bpy.types.SpaceView3D.clip_start =',bpy.types.SpaceView3D.clip_start)
print ('bpy.types.SpaceView3D.clip_start =',bpy.types.SpaceView3D.clip_end)
	
	
###
###
	
def makeMaterial(name, diffuse, specular, alpha):
	
	mat = bpy.data.materials.new(name)
	mat.diffuse_color = diffuse
	mat.diffuse_shader = 'LAMBERT'
	mat.diffuse_intensity = 1.0
	mat.specular_color = specular
	mat.specular_shader = 'COOKTORR'
	mat.specular_intensity = 0.5
	mat.alpha = alpha
	mat.ambient = 1
	
	return mat
	
###
	
def setMaterial(obj_act, mat):
	
#	me = ob.data
	me =obj_act.data
	me.materials.append(mat)
	
###
	
####### 
class lightingpanel(bpy.types.Panel):
	bl_label = "Lighting Wizard"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOL_PROPS"
	
	def draw(self, context):
	
		layout = self.layout
		scene = context.scene
	
	
		#Draw Info Box
		col2 = layout.box()
		col2.label('Scene Info:',icon='INFO')
	
		global minx , miny,minz,maxx,maxy,maxz,energymult
	
	
		global s_padding
	
		minx = 0
		miny = 0
		minz = 0
	
		maxx = 0
		maxy = 0
		maxz = 0
	
		firsttime = True
	
		#Calculate Scene Size
		for o in bpy.context.scene.objects[:]:
				bounds = functions.getobjectBounds(o)
		
				oxmin = bounds[0][0]
				oxmax = bounds[1][0]
	
				oymin = bounds[0][1]
				oymax = bounds[1][1]
	
				ozmin = bounds[0][2]
				ozmax = bounds[1][2]
	
				if oxmin <= minx:
					minx = oxmin
				if oymin <= miny:
					miny = oymin
				if ozmin <= minz:
					minz = ozmin
	
				if oxmax >= maxx:
					maxx = oxmax
				if oymax >= maxy:
					maxy = oymax
				if ozmax >= maxz:
					maxz = ozmax
		
		col2.label('Scene X Bounds: {' + str(round(minx,3)) + ',' + str(round(maxx,3)) + '}')
		col2.label('Scene Y Bounds: {' + str(round(miny,3)) + ',' + str(round(maxy,3)) + '}')
		col2.label('Scene Z Bounds: {' + str(round(minz,3)) + ',' + str(round(maxz,3)) + '}')
	
		minx = minx - s_padding
		miny = miny - s_padding
		minz = minz - s_padding
	
		maxx = maxx + s_padding
		maxy = maxy + s_padding
		maxz = maxz + s_padding
	
		#Draw Preset Options Box
		scn = bpy.context.scene
		col = layout.box()
                	
		col.label('Preset Options:',icon='INFO')
		col.prop(scn, 'menu_options')					# Main menu Level 1
	
		menu_options = context.scene.menu_options
		menu_choice = context.scene.my_menu_choice
		skydome_menu= context.scene.skydome_menu
		menu_world= context.scene.menu_world
		menu_AO= context.scene.menu_AO
		menu_Fluo= context.scene.menu_Fluo
		menu_gen= context.scene.menu_gen
		menu_other= context.scene.menu_other
		menu_special= context.scene.menu_special
		menu_angmap1= context.scene.menu_angmap1
	
	
		#### FOR STUDIO LIGHTING ####
	
		if int(menu_options)==1:					# Main menu Level 1  menu = 1
			col.prop(scn, 'my_menu_choice')					# Main menu Level 2 
	
			#### ONE POINT LIGHTING ####
			if int(menu_choice)==1: 							# Main menu Level 3  
				col.prop(scn, 'menu_one_point')
	
			#### TWO POINT LIGHTING ####
			if int(menu_choice)==2:   							# Main menu Level 3 
				col.prop(scn, 'menu_two_point')
	
			#### THREE POINT LIGHTING ####  
			if int(menu_choice)==3: 							# Main menu Level 3   
				col.prop(scn, 'menu_three_point')
	
			#### FOUR POINT LIGHTING ####   
			if int(menu_choice)==4:								# Main menu Level 3 
				col.prop(scn, 'menu_four_point')
		
		#### FOR ExteriorLIGHTING ####   
		if int(menu_options)==2:				# Main menu Level 1  menu = 2 
			col.prop(scn, 'menu_outdoor')					# Main menu Level 2
	
		#### FOR World light set up ####   
		if int(menu_options)==3:				# Main menu Level 1  menu = 3
			col.prop(scn, 'menu_world')					# Main menu Level 2
	
		#### AO  light set up ####   
		if int(menu_options)==4:				# Main menu Level 1  menu = 4
			col.prop(scn, 'menu_AO')					# Main menu Level 2
	
		#### Sky Dome  light set up ####   
		if int(menu_options)==5:					# Main menu Level 1  menu = 5
			col.prop(scn, 'skydome_menu')					# Main menu Level 2
	
			print ('skydome_menu  =',skydome_menu)
	
			if skydome_menu=="1":
	
				print ('inside  sky dome   propr')
				if scene.Ckeckskydomebright1 == True:
					col.label(' High Contrast 2 Lamps  Set', 'LAMP_AREA')
					print (' selected : High Contrast 2 Lamps  Set up #1')
					tx2="Low contrast 1"
				else:
					col.label(' Standard 2 Lamps  Set up', 'LAMP_AREA')
					print (' selected :Standard 2 Lamps  Set up #2')
					tx2="High contrast 2"
	
				col.prop(scene, "Ckeckskydomebright1", text = tx2)
				col.prop(scene, "skydomeradius")
	
		#### Fluo light set up ####   
		if int(menu_options)==6:					# Main menu Level 1  menu = 6
			col.prop(scn, 'menu_Fluo')						# Main menu Level 2
	
		#### General light set up ####   
		if int(menu_options)==7:					# Main menu Level 1  menu = 7
			col.prop(scn, 'menu_gen')						# Main menu Level 2
	
		#### Special Light set up ####   
		if int(menu_options)==8:					# Main menu Level 1  menu = 8
			col.prop(scn, 'menu_special')					# Main menu Level 2
	
		#### Other light set up ####   
		if int(menu_options)==9:					# Main menu Level 1  menu = 9
			col.prop(scn, 'menu_other')						# Main menu Level 2
	
		if int(menu_options)==10:					# Main menu Level 1  menu = 9
			col.prop(scn, 'menu_angmap1')						# Main menu Level 2
	
		#### OPERATIONS PANEL ####
		col = layout.box()  
		col.label('Operations:',icon='INFO')
		col.prop(scn, 'use_addon_objects')  
		col.operator('.add_op')
		col.operator('.remove_op')
	
##################
#### ADD LIGHTING SETUP OPERATOR ####   
	
class addOperator(bpy.types.Operator):
	bl_idname = '.add_op'
	bl_label = 'Add Current Light Preset' 
	
	def execute(self, context):
	
		menu_options = context.scene.menu_options
		menu_choice = context.scene.my_menu_choice
		menu_one_point = context.scene.menu_one_point
		menu_two_point = context.scene.menu_two_point
		menu_three_point = context.scene.menu_three_point
		menu_four_point = context.scene.menu_four_point
		skydome_menu = context.scene.skydome_menu
		menu_outdoor = context.scene.menu_outdoor 
		menu_world=menu_world= context.scene.menu_world 
		menu_AO= context.scene.menu_AO
		menu_Fluo= context.scene.menu_Fluo
		menu_gen= context.scene.menu_gen
		menu_other= context.scene.menu_other
		menu_special= context.scene.menu_special
		menu_angmap1= context.scene.menu_angmap1
	
		type_of_lighting_added = context.scene.type_of_lighting_added
	
		defaultworld1()						#  Reset  World setting to default
	
		if int(menu_options)==1: # studio lighting!
	
			if int(menu_choice)==1:
				choices = \
					{
					1 : {"name" : "Point,One Point Omindirectional", "func" : point_one_point_lighting},
					2 : {"name" : "Spot,One Point Beam", "func" : spot_one_point_lighting},
					3 : {"name" : "Area,One Area Light ", "func" : scene_one_area_lighting},
					4 : {"name" : "Hemi,One Hemi Light", "func" : scene_one_hemi_lighting},
					5 : {"name" : "Volumetric Spot,One Spot Light ", "func" : scene_one_volumetric_lighting},
					}
	
				menu_one_point = int(menu_one_point)
				if menu_one_point in choices :
					choice = choices[menu_one_point]
					type_of_lighing_added = choice["name"]
					choice["func"]()
				else : print ("FAILED"+choice["name"])
	
			elif int(menu_choice)==2:
				choices = \
					{ 
					1 : {"name" : "Two Light High constrast 1", "func" :  Addaddhc1},
					2 : {"name" : "Two Light High constrast 2", "func" :  Addaddhc2},
					3 : {"name" : "Two Light High constrast 2", "func" :  scene_two_point_lighting_behind},
					4 : {"name" : "Two Light High constrast 2", "func" :  scene_two_point_lighting_dramatic},
					}
	
				menu_two_point = int(menu_two_point)
				if menu_two_point in choices :
					choice = choices[menu_two_point]
					type_of_lighting_added = choice["name"]
					choice["func"]()
				else : print ("FAILED"+choice["name"])
	
			elif int(menu_choice)==3:
				choices = \
					{ 
					1 : {"name" : "Three Spot Lighting", "func" : add3spotlightsetup1},
					2 : {"name" : "Three Area light ", "func" : add3arealightsetup1},
					3 : {"name" : "Three Point Backlit Wall", "func" : studio_three_point_lighting_backlit_wall}
					}
	
				menu_three_point = int(menu_three_point)
				if menu_three_point in choices :
					choice = choices[menu_three_point]
					type_of_lighting_added = choice["name"]
					choice["func"]()
				else : print ("FAILED"+choice["name"])
	
			elif int(menu_choice)==4:
				choices = \
					{
					1 : {"name" : "Four Spot Light", "func" : add3spotlightsetup1},
					2 : {"name" : "Four Point Effect", "func" : studio_four_point_lighting_effect}
					}
	
				menu_four_point = int(menu_four_point)
				if menu_four_point in choices :
					choice = choices[menu_four_point]
					type_of_lighting_added = choice["name"]
					choice["func"]()
				else : print ("FAILED"+choice["name"])
	
		if int(menu_options)==2:	# Exterior set up lighting!
			choices = \
				{
				1 : {"name" : "Day light set up", "func" : addBasicsdaylight1},
				2 : {"name" : "Cloudy day", "func" : adddaycloud22},
				3 : {"name" : "Overcast day", "func" : func101},
				4 : {"name" : "Sun rise", "func" : func102},
				5 : {"name" : "Sun set", "func" : func103},
				6 : {"name" : "Clear night", "func" :Adddayclearnight42 },
				7 : {"name" : "Overcast cloudy night", "func" : Adddaycloudynight52},
				8 : {"name" : "Quarter Moon Lighting", "func" : outdoor_quarter_moon_lighting},
				9 : {"name" : "Half Moon Lighting", "func" : outdoor_half_moon_lighting},
				10 : {"name" : "Three-Quarter Moon Lighting", "func" : outdoor_three_quarter_lighting},
				11 : {"name" : "Full Moon Lighting", "func" : outdoor_full_moom_lighting},
				12 : {"name" : "Night No Moon", "func" : outdoor_night_no_moon}
				}
	
			menu_outdoor = int(menu_outdoor)
			if menu_outdoor in choices :
				choice = choices[menu_outdoor]
				type_of_lighting_added = choice["name"]
				choice["func"]()
			else : print ("FAILED" + choice["name"])
	
		if int(menu_options)==3:	# World set up lighting!
			choices = \
				{
				1 : {"name" : "Environment ", "func" : Addenvironment1},
				2 : {"name" : "Indirect", "func" : Addindirect1},
				3 : {"name" : "Indirect/Environment mixed light set up", "func" : outdoor_midday_lighting},
				4 : {"name" : "Other World set up", "func" : outdoor_night_no_moon}
				}
	 
			menu_world = int(menu_world)
			if menu_world in choices :
				choice = choices[menu_world]
				type_of_lighting_added = choice["name"]
				choice["func"]()
			else : print ("FAILED" + choice["name"])
	 
		if int(menu_options)==4:  # AO set up lighting
			choices = \
				{
				1 : {"name" : "AO Light set up", "func" : Addao1},								# Approximate Ambient Occlusion
				2 : {"name" : "AO  indirect set up", "func" : Addaoindirect1},					# Approximate Ambient Occlusion + Indirect
				3 : {"name" : "FAke AO  16 LAmps", "func" :  Add_fakeaocirclelight16},			# Fake AO with 16 lamps
				4 : {"name" : "AAO Light set up", "func" : Addaao1}							# Approximate Ambient Occlusion
				}
	
			menu_AO= int(menu_AO)
			if menu_AO in choices :
				choice = choices[menu_AO]
				type_of_lighting_added = choice["name"]
				choice["func"]()
			else : print ("FAILED" + choice["name"])
	 
		if int(menu_options)==5:	# SKy dome  / GI lighting set up 
			choices = \
				{
				1 : {"name" : "SKy Dome 1", "func" : addskydome1},
				2 : {"name" : "SKy dome / GI Ind lighting set up", "func" : addfakegi},
				} 
	 
			skydome_menu= int(skydome_menu)
			if skydome_menu in choices :
				choice = choices[skydome_menu]
				type_of_lighting_added = choice["name"]
				choice["func"]()
			else : print ("FAILED" + choice["name"])
	 
		if int(menu_options)==6:	# Fluo  lighting set up 
			choices = \
				{
				1 : {"name" : "2 X 4 Fluo Transp refractor", "func" : outdoor_sunrise_lighting},
				2 : {"name" : "1 X 4 Fluo / Fin set up", "func" : outdoor_early_morning_lighting},
				3 : {"name" : "Fluo Strips", "func" : outdoor_midday_lighting},
				4 : {"name" : "Fluo Strips Deco", "func" : outdoor_night_no_moon},
				5 : {"name" : "Fluo Watertight", "func" : outdoor_sunset_lighting},
				6 : {"name" : "Fluo Industriel", "func" : outdoor_day_moon_lighting},
				7 : {"name" : "Fluo Other", "func" : outdoor_quarter_moon_lighting}
				} 
	 
			menu_Fluo= int(menu_Fluo)
			if menu_Fluo in choices :
				choice = choices[menu_Fluo]
				type_of_lighting_added = choice["name"]
				choice["func"]()
			else : print ("FAILED"+choice["name"]) 

		if int(menu_options)==7:	# General render
			choices = \
				{
				1 : {"name" : "Clay  Render", "func" : clayrender1},
				2 : {"name" : "Sepia Photo Render", "func" : sepiarenderscene1},
				3 : {"name" : "Sepia Scene Render", "func" : sepiarenderscene1},
				4 : {"name" : "Sketchup style Render", "func" : Addsketchup1operator1}
				}
	 
			menu_gen= int(menu_gen)
			if menu_gen in choices :
				choice = choices[menu_gen]
				type_of_lighting_added = choice["name"]
				choice["func"]()
			else : print ("FAILED"+choice["name"]) 
	 
		if int(menu_options)==8:	# Special Light set up
			choices = \
				{
				1 : {"name" : "Area Light Set up", "func" : outdoor_sunrise_lighting},
				2 : {"name" : "Studio Light Set up", "func" : Addstudio1},
				3 : {"name" : "Light Box 3", "func" : addlightbox33},
				4 : {"name" : "Light Box 4", "func" : addlightbox34},
				5 : {"name" : "Theather light / smoke", "func" : Addtheater1},
				6 : {"name" : "Theather 3 color light / smoke", "func" : outdoor_sunset_lighting}
				} 
	 
			menu_special= int(menu_special)
			if menu_special in choices :
				choice = choices[menu_special]
				type_of_lighting_added = choice["name"]
				choice["func"]()
			else : print ("FAILED"+choice["name"]) 
	
		if int(menu_options)==9:	# Other Light set up
			choices = \
				{
				1 : {"name" : "Camera Isometric Set up", "func" : addisocam1},
				2 : {"name" : "Camera Dimetric Set up", "func" : outdoor_early_morning_lighting},
				3 : {"name" : "Camera Trimetric Set up", "func" : outdoor_midday_lighting}
				} 
	
			menu_other= int(menu_other)
			if menu_other in choices :
				choice = choices[menu_other]
				type_of_lighting_added = choice["name"]
				choice["func"]()
			else : print ("FAILED"+choice["name"]) 
	
		if int(menu_options)==10:	# Ang sky HDRI map set up
			choices = \
				{
				1 : {"name" : "Angular map Set up", "func" : world_Angularmap1},
				2 : {"name" : "Sky map Set up", "func" : world_skymap1},
				3 : {"name" : "HDRI map Set up", "func" : world_HDRI1}
				} 
	
			menu_angmap1= int(menu_angmap1)
			if menu_angmap1 in choices :
				choice = choices[menu_angmap1]
				type_of_lighting_added = choice["name"]
				choice["func"]()
			else : print ("FAILED"+choice["name"]) 
	
			menu_other= int(menu_other)
			if menu_other in choices :
				choice = choices[menu_other]
				type_of_lighting_added = choice["name"]
				choice["func"]()
			else : print ("FAILED"+choice["name"]) 
	
		print ('added '+ choice["name"])
	
		return {'FINISHED'}
	
##################
#### OBJECT REMOVAL OPERATOR ####   
	
class removeOperator(bpy.types.Operator):
	
	bl_idname = '.remove_op'
	bl_label = 'Remove Objects/Lamps'
	
	def execute(self, context):
	
		self.report({'INFO'}, "Removed Objects/Lamps added with the wizard")
	
		if self.report:
			bpy.ops.object.select_by_type(extend=False,type='LAMP')
			bpy.ops.object.delete()
		print ('removed objects/lamps from scene')
	
	
		bpy.context.scene.world.texture_slots.clear(0)
		bpy.context.scene.world.texture_slots.clear(1)
		bpy.context.scene.world.texture_slots.clear(2)
		bpy.context.scene.world.texture_slots.clear(3)
		bpy.context.scene.world.texture_slots.clear(4)
	
		bpy.context.scene.render.use_edge_enhance = False
	
	
		bpy.ops.object.select_pattern(extend=False, pattern="Skydome", case_sensitive=False)
		ob1 = bpy.context.object
		bpy.ops.object.delete()
	
		bpy.ops.object.select_pattern(extend=False, pattern="Softbox", case_sensitive=False)
		ob1 = bpy.context.object
		bpy.ops.object.delete()
	
		bpy.ops.object.select_pattern(extend=False, pattern="new_empty", case_sensitive=False)
		ob1 = bpy.context.object
		bpy.ops.object.delete()
	
		bpy.ops.object.select_pattern(extend=False, pattern="empty1", case_sensitive=False)
		ob1 = bpy.context.object
		bpy.ops.object.delete()
	
		bpy.ops.object.select_pattern(extend=False, pattern="90degreeswall1", case_sensitive=False)
		ob1 = bpy.context.object
		bpy.ops.object.delete()
	
		bpy.ops.object.select_pattern(extend=False, pattern="reflect1", case_sensitive=False)
	
		ob1 = bpy.context.object
		bpy.ops.object.delete()
	
		bpy.ops.object.select_pattern(extend=False, pattern="reflect2", case_sensitive=False)
		ob1 = bpy.context.object
		bpy.ops.object.delete()
	
		return {'FINISHED'}
	
##################
class functions():
	
	def getobjectBounds(ob):
	
		obminx = ob.location.x
		obminy = ob.location.y
		obminz = ob.location.z
	
		obmaxx = ob.location.x
		obmaxy = ob.location.y
		obmaxz = ob.location.z
	
		for vertex in ob.bound_box[:]:
			x = ob.location.x + (ob.scale.x * vertex[0])
			y = ob.location.y + (ob.scale.y * vertex[1])
			z = ob.location.z + (ob.scale.z * vertex[2])
	
			if x <= obminx:
				obminx = x
			if y <= obminy:
				obminy = y
			if z <= obminz:
				obminz = z
	
			if x >= obmaxx:
				obmaxx = x
			if y >= obmaxy:
				obmaxy = y
			if z >= obmaxz:
				obmaxz = z
		
		boundsmin = [obminx,obminy,obminz]
		boundsmax = [obmaxx,obmaxy,obmaxz] 

		bounds = [boundsmin,boundsmax]
		return bounds
	
	def addTrackToConstraint(ob, name, target):
		cns = ob.constraints.new('TRACK_TO')
		cns.name = name
		cns.target = target
		cns.track_axis = 'TRACK_NEGATIVE_Z'
		cns.up_axis = 'UP_Y'
		cns.owner_space = 'WORLD'
		cns.target_space = 'WORLD'
		return
	
	def getDistance(object1, object2):  
		location1x = object1.location.x
		location2x = object2.location.x
	 
		location1y = object1.location.y
		location2y = object2.location.y
	 
		location1z = object1.location.z
		location2z = object2.location.z
	 
		distancex = location2x - location1x
		distancey = location2y - location1y
		distancez = location2z - location1z
	  
		Sqdistancex = distancex * distancex
		Sqdistancey = distancey * distancey
		Sqdistancez = distancez * distancez
	
		SumDistances = Sqdistancex + Sqdistancey + Sqdistancez
		return math.sqrt(SumDistances)
	
#############
#### one point , ONE POINT LIGHTING FUNCTIONS ####
def studio_world_settings():
	world = bpy.context.scene.world
	world.name = 'studio'
	world.horizon_color = (0,0,0)
	world.zenith_color = (0,0,0)
	world.ambient_color = (0,0,0)
	
##################
# ONE POINT
def point_one_point_lighting():
	
	global layers
	global minx , miny,minz,maxx,maxy,maxz,energymult
	
	#Place Empty at the center of the scene
	
	minx = minx + 1
	miny = miny + 1
	minz = minz + 1
	
	maxx = maxx - 1
	maxy = maxy - 1
	maxz = maxz - 1
	
	midx = (minx + maxx) /2
	midy = (miny + maxy) /2
	midz = (minz + maxz) /2
	
	bpy.ops.object.lamp_add(type='POINT', view_align=False, location=(-5.2040252685546875, -1.720866084098816, 7.146382591247559), rotation=(0.36103200912475586, -0.4932146966457367, -0.16780202090740204), layers=(layers))
	
	lamp1 = bpy.context.object
	
	lamp1.location.x = midx
	lamp1.location.y = midy+2
	lamp1.location.z = maxz
	
	key = bpy.context.object
	
	#Set Lamp energy
	m = .15
	lampD = functions.getDistance(key, Empty)
	lampE = (lampD * m)
	
	print (' lampd d=',lampD,' lamp E=',lampE)
	print (' minx =',minx,'  miny =',miny,'  minz =',minz)
	print (' max =',maxx,'  may =',maxy,'  maz =',maxz)
	print (' midx =',midx,' midy =',midy,' midz =',midz)
	
	### Configure Lighting Setup ###
	lamp1.name = 'Point1'								# Point light  name
	
	
	lamp1.data.energy = lampE
	lamp1.data.distance = lampD 
	lamp1.data.shadow_method = 'RAY_SHADOW'
	lamp1.data.color=(1.0,1.0,1.0)						# White   point lamp
	
# No constraint here  cause it's an omnidirectional lamp
	print ("Function =", "Point light one_point_lighting")
	
#######
# ONE POINT
def spot_one_point_lighting():
	
	global layers
	global minx , miny,minz,maxx,maxy,maxz,energymult
	
	midx = (minx + maxx) /2
	midy = (miny + maxy) /2
	midz = (minz + maxz) /2
	
	bpy.ops.object.select_pattern(extend=False, pattern="Empty", case_sensitive=False)
	key1 = bpy.context.object
	key1.location.x = midx
	key1.location.y = midy
	key1.location.z = midz
	
	print (' midx =',midx,' midy =',midy,' midz =',midz)
	
	bpy.ops.object.lamp_add(type='SPOT',view_align=False,
		location=(-5.2040252685546875, -1.720866084098816, 7.146382591247559),
		rotation=(0.36103200912475586, -0.4932146966457367, -0.16780202090740204))
	
	lamp1 = bpy.context.object
	lamp1.name = 'spot1'

	key = bpy.context.object
	
	#Set Lamp energy
	m = .15
	lampD = functions.getDistance(key, key1)
	lampE = (lampD * m)

	### Configure Lighting Setup ###
	key.name = 'Spot1'							# Spot light  name
	
	key.data.energy = lampE
	key.data.distance = lampD
	key.data.spot_size = 3.141593
	key.data.spot_blend = 1
	key.data.shadow_method = 'BUFFER_SHADOW'
	key.data.shadow_buffer_type = 'HALFWAY'
	key.data.shadow_filter_type = 'GAUSS'
	key.data.shadow_buffer_soft = 10
	key.data.shadow_buffer_size = 2048
	key.data.shadow_buffer_bias = 0.100
	key.data.shadow_buffer_samples = 8
	key.data.use_auto_clip_start = True
	key.data.use_auto_clip_end = True
	
	key.location.z = maxz
	key.location.x = minx
	key.location.y = midy
	
	key.data.color=(1.0,1.0,1.0)						# Std Spot light   white
	
	
	#Add Track Constraints
	functions.addTrackToConstraint(lamp1,'AutoTrack',key1)
	
	print ("Function =", "Spot light one_point_lighting")
	
##################
# GLOBAL
def scene_one_point_lighting_global():
	
	global layers
	global minx , miny,minz,maxx,maxy,maxz,energymult
	
	midx = (minx + maxx) /2
	midy = (miny + maxy) /2
	midz = (minz + maxz) /2
	
	studio_world_settings()
	
	bpy.ops.object.add(type='EMPTY', view_align=False, enter_editmode=False, location=(12.7992, 6.42344, -4.98939), rotation=(0, 0, 0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
	empty = bpy.context.object
	
	empty.location.x = midx
	empty.location.y = midy
	empty.location.z = midz
	
	bpy.ops.object.lamp_add(type='HEMI',view_align=False,
		location=(-5.2040252685546875, -1.720866084098816, 7.146382591247559),
		rotation=(0.36103200912475586, -0.4932146966457367, -0.16780202090740204))
	
	key = bpy.data.objects.get('Hemi')
	
	#Set Lamp energy
	m = .15
	lampD = functions.getDistance(key, empty)
	lampE = (lampD * m)

	
	key.name = 'ONE_POINT_GLOBAL_KEY'
	key.data.color = (0.853, 1.0, 1.0)
	key.data.distance = lampD
	key.data.energy = lampE
	key.location.x = minx
	key.location.y = midy
	key.location.z = maxz
	
	print ("Function =", "scene_one_point_lighting_global")
	
##################
# Hemi Light
def scene_one_hemi_lighting():
	
	global layers
	global minx , miny,minz,maxx,maxy,maxz,energymult
	
	midx = (minx + maxx) /2
	midy = (miny + maxy) /2
	midz = (minz + maxz) /2
	
	studio_world_settings()
	
	bpy.ops.object.add(type='EMPTY', view_align=False, enter_editmode=False, location=(12.7992, 6.42344, -4.98939), rotation=(0, 0, 0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
	empty = bpy.context.object
	
	empty.location.x = midx
	empty.location.y = maxy
	empty.location.z = midz
	
	bpy.ops.object.lamp_add(type='HEMI', view_align=False, location=(-5.2040252685546875, -1.720866084098816, 7.146382591247559), rotation=(1.537930, 0.711540, 3.687180), layers=(layers))

	lamp1 = bpy.context.object	
	lamp1.name = 'hemi1'
	
	#Set Lamp energy
	m = .15
	lampD = functions.getDistance(lamp1, empty)
	lampE = (lampD * m)


	lamp1.data.energy = lampE
	lamp1.data.distance = lampD
	lamp1.data.color=(0.385,0.212,0.212) # Brownish   Hemi lamp
	lamp1.location.x = minx
	lamp1.location.y = midy
	lamp1.location.z = maxz
	
	functions.addTrackToConstraint(lamp1, "hemi1", empty)
	
	print ("Function =", "scene_one_hemi_lighting")
	
##################
# Area  
def scene_one_area_lighting():
	
	global layers
	global minx , miny,minz,maxx,maxy,maxz,energymult
	
	midx = (minx + maxx) /2
	midy = (miny + maxy) /2
	midz = (minz + maxz) /2
	
	studio_world_settings()	
														# Add area lamp
	bpy.ops.object.add(type='EMPTY', view_align=False, enter_editmode=False, location=(12.7992, 6.42344, -4.98939), rotation=(0, 0, 0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
	empty = bpy.context.object
	
	empty.location.x = midx
	empty.location.y = midy
	empty.location.z = minz
	
	bpy.ops.object.lamp_add(type='AREA', view_align=False, location=(0, 0, 9), rotation=(0, 0, 0), layers=(layers))  
	lamp1 = bpy.context.object
	
	#Set Lamp energy
	m = .05
	lampD = functions.getDistance(lamp1, empty)
	lampE = (lampD * m)
	
	lamp1.name = 'area1'
	
	lamp1.location.x = midx
	lamp1.location.y = midy
	lamp1.location.z = maxz
	
	lamp1.data.energy = lampE
	lamp1.data.distance = lampD
	lamp1.data.gamma = 1
	lamp1.data.shadow_method = 'RAY_SHADOW'
	lamp1.data.color=(1.0,1.0,1.0)											# Area lamp
	lamp1.data.size = 10
	
	print ("Function =", "scene_one_area_lighting")
	
##################
# ONE volumetric spot light
def scene_one_volumetric_lighting():
	
	global layers
	global minx , miny,minz,maxx,maxy,maxz,energymult
	
	midx = (minx + maxx) /2
	midy = (miny + maxy) /2
	midz = (minz + maxz) /2
	
	
	bpy.ops.object.add(type='EMPTY', view_align=False, enter_editmode=False, location=(12.7992, 6.42344, -4.98939), rotation=(0, 0, 0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
	empty = bpy.context.object
	
	empty.location.x = midx
	empty.location.y = maxy
	empty.location.z = midz
	
	bpy.ops.object.lamp_add(type='SPOT',view_align=False,
		location=(-5.2040252685546875, -1.720866084098816, 7.146382591247559),
		rotation=(0.36103200912475586, -0.4932146966457367, -0.16780202090740204))
	
	key = bpy.context.object
	
	### Configure Lighting Setup ###
	key.name = 'Spot1'							# Spot light  name
	
	#Set Lamp energy
	m = .15
	lampD = functions.getDistance(key, empty)
	lampE = (lampD * m)
		
	key.data.energy = lampE
	key.data.distance = lampD
	key.data.use_halo = True
	key.data.spot_size = 1.745330
	key.data.halo_intensity = .05
	key.data.spot_blend = 1
	key.data.shadow_method = 'BUFFER_SHADOW'
	key.data.shadow_buffer_type = 'HALFWAY'
	key.data.shadow_filter_type = 'GAUSS'
	key.data.shadow_buffer_soft = 10
	key.data.shadow_buffer_size = 2048
	key.data.shadow_buffer_bias = 0.100
	key.data.shadow_buffer_samples = 8
	key.data.use_auto_clip_start = True
	key.data.use_auto_clip_end = True
	
	key.location.x = minx
	key.location.y = miny
	key.location.z = midz
	
	key.data.color=(1.0,0,0)						# Std Spot light  red
	
	functions.addTrackToConstraint(key, "Spot1", empty)

	print ("Function =", "scene_one_volumetric_lighting")
	
##################
#### STUDIO, TWO POINT LIGHTING FUNCTIONS ####
# TWO POINT
def scene_two_point_lighting():
	
	studio_world_settings()
	
	bpy.ops.object.lamp_add(type='SPOT',view_align=False,
		location=(-9.779207229614258, -7.4978718757629395, 8.056272506713867), 
		rotation=(0.491294801235199, -0.8801535964012146, -0.08902067691087723))
	
	bpy.ops.object.lamp_add(type='SPOT',view_align=False,
		location=(17.35930633544922, -6.029705047607422, 8.019586563110352), 
		rotation=(1.1428003311157227, -0.0401807576417923, 1.2666490077972412))
	
	key = bpy.data.objects.get('Spot')
	key.name = 'TP_KEY'
	key.data.energy = 5.301
	key.data.spot_blend = 1
	
	fill = bpy.data.objects.get('Spot.001')
	fill.name = 'TP_FILL'
	fill.data.energy = 5.856
	fill.data.spot_blend = 1
	print ("Function =", "scene_two_point_lighting")
	
##################
# BEHIND
def scene_two_point_lighting_behind():
	
	studio_world_settings()
	
	bpy.ops.object.lamp_add(type='SPOT',view_align=False,
		location=(-10.325093269348145, -8.980795860290527, 5.326213359832764), 
		rotation=(0.6505584716796875, -1.0884696245193481, --0.11806187778711319))
	
	bpy.ops.object.lamp_add(type='AREA',view_align=False,
		location=(-0.4397315979003906, 19.942474365234375, 1.134472370147705), 
		rotation=(1.4984596967697144, -0.05649565905332565, 3.1783173084259033))
	
	key = bpy.data.objects.get('Spot')
	key.name = 'TWO_POINT_BEHIND_KEY'
	key.data.energy = 5.301
	key.data.spot_blend = 1
	
	fill = bpy.data.objects.get('Area')
	fill.name = 'TWO_POINT_BEHIND_FILL'
	fill.data.energy = 1.234
	fill.data.shadow_method = 'RAY_SHADOW'
	print ("Function =", "scene_two_point_lighting_behind")
	
##################
# DRAMATIC
def scene_two_point_lighting_dramatic():
	
	studio_world_settings()
	
	bpy.ops.object.lamp_add(type='SPOT',view_align=False,
		location=(-9.779207229614258, -7.4978718757629395, 8.056272506713867), 
		rotation=(0.491294801235199, -0.8801535964012146, -0.08902067691087723))
	
	bpy.ops.object.lamp_add(type='SPOT',view_align=False,
		location=(17.35930633544922, -6.029705047607422, 8.019586563110352), 
		rotation=(1.1428003311157227, -0.0401807576417923, 1.2666490077972412))
	
	key = bpy.data.objects.get('Spot')
	key.name = 'TWO_POINT_DRAMITIC_KEY'
	key.data.energy = 5.301
	key.data.spot_blend = 1
	
	fill = bpy.data.objects.get('Spot.001')
	fill.name = 'TWO_POINT_DRAMATIC_FILL'
	fill.data.energy = 5.856
	fill.data.spot_blend = 1
	print ("Function =", "scene_two_point_lighting_dramatic")
	
##################
# WHITE
def scene_two_point_lighting_white():
	
	studio_world_settings()
	
	bpy.ops.object.lamp_add(type='SPOT',view_align=False,
		location=(-9.779207229614258, -7.4978718757629395, 8.056272506713867), 
		rotation=(0.491294801235199, -0.8801535964012146, -0.08902067691087723))
	
	bpy.ops.object.lamp_add(type='SPOT',view_align=False,
		location=(17.35930633544922, -6.029705047607422, 8.019586563110352), 
		rotation=(1.1428003311157227, -0.0401807576417923, 1.2666490077972412))
	
	key = bpy.data.objects.get('Spot')
	key.name = 'TWO_POINT_WHITE_KEY'
	key.data.energy = 5.301
	key.data.spot_blend = 1
	
	fill = bpy.data.objects.get('Spot.001')
	fill.name = 'TWO_POINT_WHITE_FILL'
	fill.data.energy = 5.856
	fill.data.spot_blend = 1
	print ("Function =", "scene_two_point_lighting_white")
	
##################
# WHITE BIS 
def scene_two_point_lighting_white_bis():
	
	studio_world_settings()
	
	bpy.ops.object.lamp_add(type='SPOT',view_align=False,
		location=(-9.779207229614258, -7.4978718757629395, 8.056272506713867), 
		rotation=(0.491294801235199, -0.8801535964012146, -0.08902067691087723))
	
	bpy.ops.object.lamp_add(type='SPOT',view_align=False,
		location=(17.35930633544922, -6.029705047607422, 8.019586563110352), 
		rotation=(1.1428003311157227, -0.0401807576417923, 1.2666490077972412))
	
	key = bpy.data.objects.get('Spot')
	key.name = 'TWO_POINT_WHITEBIS_KEY'
	key.data.energy = 5.301
	key.data.spot_blend = 1
	
	fill = bpy.data.objects.get('Spot.001')
	fill.name = 'TWO_POINT_WHITEBIS_FILL'
	fill.data.energy = 5.856
	fill.data.spot_blend = 1
	print ("Function =", "scene_two_point_lighting_white_bis")
	
##################
# BLUE  
def scene_two_point_lighting_blue():
	
	studio_world_settings()
	
	bpy.ops.object.lamp_add(type='SPOT',view_align=False,
		location=(-9.779207229614258, -7.4978718757629395, 8.056272506713867), 
		rotation=(0.491294801235199, -0.8801535964012146, -0.08902067691087723))
	
	bpy.ops.object.lamp_add(type='SPOT',view_align=False,
		location=(17.35930633544922, -6.029705047607422, 8.019586563110352), 
		rotation=(1.1428003311157227, -0.0401807576417923, 1.2666490077972412))
	
	key = bpy.data.objects.get('Spot')
	key.name = 'TWO_POINT_BLUE_KEY'
	key.data.energy = 5.301
	key.data.spot_blend = 1
	
	fill = bpy.data.objects.get('Spot.001')
	fill.name = 'TWO_POINT_BLUE_FILL'
	fill.data.energy = 5.856
	fill.data.spot_blend = 1
	print ("Function =", "scene_two_point_lighting_blue")
	
##################
# FLOATING  
def scene_two_point_lighting_floating():
	
	studio_world_settings()
	
	bpy.ops.object.lamp_add(type='SPOT',view_align=False,
		location=(-9.779207229614258, -7.4978718757629395, 8.056272506713867), 
		rotation=(0.491294801235199, -0.8801535964012146, -0.08902067691087723))
	
	bpy.ops.object.lamp_add(type='SPOT',view_align=False,
		location=(17.35930633544922, -6.029705047607422, 8.019586563110352), 
		rotation=(1.1428003311157227, -0.0401807576417923, 1.2666490077972412))
	
	key = bpy.data.objects.get('Spot')
	key.name = 'TWO_POINT_FLOATING_KEY'
	key.data.energy = 5.301
	key.data.spot_blend = 1
	
	fill = bpy.data.objects.get('Spot.001')
	fill.name = 'TWO_POINT_FLOATING_FILL'
	fill.data.energy = 5.856
	fill.data.spot_blend = 1
	print ("Function =", "scene_two_point_lighting_floating")
	
##################
# ROOM  
def scene_two_point_lighting_room():
	
	studio_world_settings()
	
	bpy.ops.object.lamp_add(type='SPOT',view_align=False,
		location=(-9.779207229614258, -7.4978718757629395, 8.056272506713867), 
		rotation=(0.491294801235199, -0.8801535964012146, -0.08902067691087723))
	
	bpy.ops.object.lamp_add(type='SPOT',view_align=False,
		location=(17.35930633544922, -6.029705047607422, 8.019586563110352), 
		rotation=(1.1428003311157227, -0.0401807576417923, 1.2666490077972412))
	
	key = bpy.data.objects.get('Spot')
	key.name = 'TWO_POINT_ROOM_KEY'
	key.data.energy = 5.301
	key.data.spot_blend = 1
	
	fill = bpy.data.objects.get('Spot.001')
	fill.name = 'TWO_POINT_ROOM_FILL'
	fill.data.energy = 5.856
	fill.data.spot_blend = 1
	print ("Function =", "scene_two_point_lighting_room")
	
	
##################
# ROOM SPOT
def scene_two_point_lighting_room_spot():
	
	studio_world_settings()
	
	bpy.ops.object.lamp_add(type='SPOT',view_align=False,
		location=(-9.779207229614258, -7.4978718757629395, 8.056272506713867), 
		rotation=(0.491294801235199, -0.8801535964012146, -0.08902067691087723))
	
	bpy.ops.object.lamp_add(type='SPOT',view_align=False,
		location=(17.35930633544922, -6.029705047607422, 8.019586563110352), 
		rotation=(1.1428003311157227, -0.0401807576417923, 1.2666490077972412))
	
	key = bpy.data.objects.get('Spot')
	key.name = 'TWO_POINT_ROOM_KEY'
	key.data.energy = 5.301
	key.data.spot_blend = 1
	
	fill = bpy.data.objects.get('Spot.001')
	fill.name = 'TWO_POINT_ROOM_FILL'
	fill.data.energy = 5.856
	fill.data.spot_blend = 1
	print ("Function =", "scene_two_point_lighting_room_spot")
	
#### STUDIO, THREE POINT LIGHTING FUNCTIONS ####
# THREE POINT
def studio_three_point_lighting():
	
	studio_world_settings()
	
	bpy.ops.object.lamp_add(type='SPOT',view_align=False,
		location=(-9.779207229614258, -7.4978718757629395, 8.056272506713867), 
		rotation=(0.491294801235199, -0.8801535964012146, -0.08902067691087723))
	
	bpy.ops.object.lamp_add(type='SPOT',view_align=False,
		location=(17.35930633544922, -6.029705047607422, 8.019586563110352), 
		rotation=(1.1428003311157227, -0.0401807576417923, 1.2666490077972412))
	
	bpy.ops.object.lamp_add(type='SPOT',view_align=False,
		location=(-0.9802832603459, 8.697346687316895, 3.7611913681030273), 
		rotation=(1.0024033784866333, -0.6399083733558655, 3.6022660732269287))
	
	key = bpy.data.objects.get('Spot')
	key.name = 'TP_KEY'
	key.data.energy = 5.301
	key.data.spot_blend = 1
	
	fill = bpy.data.objects.get('Spot.001')
	fill.name = 'TP_FILL'
	fill.data.energy = 5.856
	fill.data.spot_blend = 1
	
	back = bpy.data.objects.get('Spot.002')
	back.name = 'TP_BACK'
	back.data.energy = 10
	back.data.distance = 40
	back.data.spot_blend = 1
	
	print ("Function =", "studio_three_point_lighting")
	
	
##################
# AUTUMN
def studio_three_point_lighting_autumn():
	
	studio_world_settings()
	
	bpy.ops.object.lamp_add(type='AREA',view_align=False,
		location=(-9.779207229614258, -7.4978718757629395, 8.056272506713867), 
		rotation=(0.491294801235199, -0.8801535964012146, -0.08902067691087723))
	
	bpy.ops.object.lamp_add(type='SPOT',view_align=False,
		location=(10.386297225952148, -14.805946350097656, 8.019586563110352), 
		rotation=(1.1428003311157227, -0.0401807576417923, 0.6262273192405701))
		
	bpy.ops.object.lamp_add(type='SPOT',view_align=False,
		location=(10.92225456237793, 56.31578063964844, 32.05726623535156), 
		rotation=(1.0024033784866333, -0.6399083733558655, 3.6022660732269287))
	
	
	key = bpy.data.objects.get('Area')
	key.name = 'TP_AUTUMN_KEY'
	key.data.color = 0.040, 0.008, 0.0 
	key.data.energy = 0.545
	
	fill = bpy.data.objects.get('Spot')
	fill.name = 'TP_AUTUMN_FILL'
	
	fill.data.energy = 0.542
	fill.data.spot_blend = 1
	fill.data.spot_size = 0.785398
	fill.data.shadow_filter_type = 'GAUSS'
	fill.data.shadow_buffer_soft = 17.400
	
	back = bpy.data.objects.get('Spot.001')
	back.name = 'TP_AUTUMN_BACK'
	back.data.energy = 1.356
	back.data.distance = 75
	back.data.spot_blend = 1
	back.data.spot_size = 0.471239
	back.data.shadow_filter_type = 'GAUSS'
	back.data.shadow_buffer_soft = 17.400
	
	if not "AutumnTex" in bpy.data.textures:
		import os
		realpath = os.path.expanduser('~/My Documents/blender mess about/autumn_tex.png')
		try:
			img = bpy.data.images.load(realpath)
		except:
			raise NameError("Cannot load image %s" % realpath)
	
		# Create image texture from image
		cTex = bpy.data.textures.new('AutumnTex', type='IMAGE')
		cTex.image = img
		cTex.use_alpha = False
		cTex.use_mipmap_gauss = True
		cTex.filter_type = 'AREA'
		cTex.filter_eccentricity = 1
		cTex.filter_size = 1.37
		cTex.use_filter_size_min = True
		autumn = bpy.data.textures.get("AutumnTex") 
		key.data.active_texture = autumn
	else:   
		autumn = bpy.data.textures.get("AutumnTex") 
		key.data.active_texture = autumn
	
	print ("Function =", "studio_three_point_lighting_autumn")
	
##################
# BACKLIT WALL  
def studio_three_point_lighting_backlit_wall():
	
	studio_world_settings()
	
	bpy.ops.object.lamp_add(type='SPOT',view_align=False,
		location=(-9.779207229614258, -7.4978718757629395, 6.8997416496276855), 
		rotation=(0.44142112135887146, -0.8970814943313599, -0.054358765482902))
	
	bpy.ops.object.lamp_add(type='SPOT',view_align=False,
		location=(17.35930633544922, -6.029705047607422, 8.019586563110352), 
		rotation=(1.1428003311157227, -0.0401807576417923, 1.2666490077972412))
	
	bpy.ops.object.lamp_add(type='SPOT',view_align=False,
		location=(0.0, 0.0, -0.947617898273468), 
		rotation=(1.5707969705062866, 0.0, 0.0))
	
	key = bpy.data.objects.get('Spot')
	key.name = 'TP_BACKLIT_KEY'
	key.data.energy = 5.454
	key.data.spot_blend = 1
	
	fill = bpy.data.objects.get('Spot.001')
	fill.name = 'TP_BACKLIT_FILL'
	fill.data.energy = 3.547
	fill.data.spot_blend = 1
	
	back = bpy.data.objects.get('Spot.002')
	back.name = 'TP_BACKLIT_BACK'
	back.data.energy = 0.423
	back.data.distance = 32.760
	back.data.spot_blend = 1
	print ("Function =", "scene_three_point_lighting_backlit_wall")
	
##################
# BLOWNOUT  
def studio_three_point_lighting_blownout():
	
	studio_world_settings()
	
	bpy.ops.object.lamp_add(type='SPOT',view_align=False,
		location=(-1.37924830661017, -6.787240982055664, 12.466023445129395), 
		rotation=(-0.27631163597106934, -0.43347325921058655, 1.7720673084259033))
	
	bpy.ops.object.lamp_add(type='SPOT',view_align=False,
		location=(0.0, 2.89731502532959, 13.485641479492188), 
		rotation=(-0.0845556692481041, -6.121555328369141, 1.1120541095733643))
	
	bpy.ops.object.lamp_add(type='SPOT',view_align=False,
		location=(1.2730222940444946, -0.4670710563659668, 16.19774627685547), 
		rotation=(0.16847357153892517, 0.00713651767000556, -4.911602973937988))
	
	key = bpy.data.objects.get('Spot')
	key.name = 'TP_BLOWNOUT_KEY'
	key.data.energy = 10
	key.data.spot_blend = 0.710
	key.data.spot_size = 0.733038
	
	fill = bpy.data.objects.get('Spot.001')
	fill.name = 'TP_BLOWNOUT_FILL'
	fill.data.energy = 3.170
	fill.data.distance = 27.260
	fill.data.spot_blend = 0.899
	fill.data.spot_size = 0.471239
	
	back = bpy.data.objects.get('Spot.002')
	back.name = 'TP_BLOWNOUT_BACK'
	back.data.energy = 6.885
	back.data.distance = 40
	back.data.spot_blend = 1
	back.data.spot_size = 0.785398 
	print ("Function =", "studio_three_point_lighting_blownout")
	
##################
# STAGE 
def scene_three_point_lighting_stage():
	
	studio_world_settings()
	
	bpy.ops.object.lamp_add(type='SPOT',view_align=False,
		location=(-1.37924830661017, -6.787240982055664, 12.466023445129395), 
		rotation=(-0.27631163597106934, -0.43347325921058655, 1.7720673084259033))
	
	bpy.ops.object.lamp_add(type='SPOT',view_align=False,
		location=(0.0, 2.89731502532959, 13.485641479492188), 
		rotation=(-0.0845556692481041, -6.121555328369141, 1.1120541095733643))
	
	bpy.ops.object.lamp_add(type='SPOT',view_align=False,
		location=(1.2730222940444946, -0.4670710563659668, 16.19774627685547), 
		rotation=(0.16847357153892517, 0.00713651767000556, -4.911602973937988))
	
	key = bpy.data.objects.get('Spot')
	key.name = 'TP_STAGE_KEY'
	key.data.energy = 10
	key.data.spot_blend = 0.710
	key.data.spot_size = 0.733038
	
	fill = bpy.data.objects.get('Spot.001')
	fill.name = 'TP_STAGE_FILL'
	fill.data.energy = 3.170
	fill.data.distance = 27.260
	fill.data.spot_blend = 0.899
	fill.data.spot_size = 0.471239
	fill.data.use_halo = True
	
	back = bpy.data.objects.get('Spot.002')
	back.name = 'TP_STAGE_BACK'
	back.data.energy = 6.885
	back.data.distance = 40
	back.data.spot_blend = 1
	back.data.spot_size = 0.526484
	back.data.use_halo = True
	print ("Function =", "scene_three_point_lighting_stage")
	
##################
# LIGHT CONE
def scene_three_point_lighting_light_cone():
	
	studio_world_settings()
	
	bpy.ops.object.lamp_add(type='SPOT',view_align=False,
		location=(-1.37924830661017, -6.787240982055664, 12.466023445129395), 
		rotation=(-0.27631163597106934, -0.43347325921058655, 1.7720673084259033))
	
	bpy.ops.object.lamp_add(type='SPOT',view_align=False,
		location=(0.0, 2.89731502532959, 13.485641479492188), 
		rotation=(-0.0845556692481041, -6.121555328369141, 1.1120541095733643))
	
	bpy.ops.object.lamp_add(type='SPOT',view_align=False,
		location=(1.2730222940444946, -0.4670710563659668, 16.19774627685547), 
		rotation=(0.16847357153892517, 0.00713651767000556, -4.911602973937988))
	
	key = bpy.data.objects.get('Spot')
	key.name = 'TP_LIGHTCONE_KEY'
	key.data.energy = 0.580
	key.data.spot_blend = 0.793
	key.data.spot_size = 0.418879
	key.data.use_halo = True
	
	fill = bpy.data.objects.get('Spot.001')
	fill.name = 'TP_LIGHTCONE_FILL'
	fill.data.energy = 0.660
	fill.data.distance = 27.260
	fill.data.spot_blend = 0.899
	fill.data.spot_size = 0.244346
	fill.data.use_halo = True
	
	back = bpy.data.objects.get('Spot.002')
	back.name = 'TP_LIGHTCONE_BACK'
	back.data.energy = 0.715
	back.data.distance = 40
	back.data.spot_blend = 1
	back.data.spot_size = 0.226893
	back.data.use_halo = True
	
	print ("Function =", "scene_three_point_lighting_light_cone")
	
##################
# BEAM 3D   
def scene_three_point_lighting_beam_3d():
	
	studio_world_settings()
	
	bpy.ops.object.lamp_add(type='SPOT',view_align=False,
		location=(-1.37924830661017, -6.787240982055664, 12.466023445129395), 
		rotation=(-0.27631163597106934, -0.43347325921058655, 1.7720673084259033))
	
	bpy.ops.object.lamp_add(type='SPOT',view_align=False,
		location=(0.0, 2.89731502532959, 13.485641479492188), 
		rotation=(-0.0845556692481041, -6.121555328369141, 1.1120541095733643))
	
	bpy.ops.object.lamp_add(type='SPOT',view_align=False,
		location=(1.2730222940444946, -0.4670710563659668, 16.19774627685547), 
		rotation=(0.16847357153892517, 0.00713651767000556, -4.911602973937988))
	
	key = bpy.data.objects.get('Spot')
	key.name = 'TP_BEAM3D_KEY'
	key.data.energy = 10
	key.data.spot_blend = 0.710
	key.data.spot_size = 0.733038
	
	fill = bpy.data.objects.get('Spot.001')
	fill.name = 'TP_BEAM3D_FILL'
	fill.data.energy = 3.170
	fill.data.distance = 27.260
	fill.data.spot_blend = 0.899
	fill.data.spot_size = 0.471239
	
	back = bpy.data.objects.get('Spot.002')
	back.name = 'TP_BEAM3D_BACK'
	back.data.energy = 6.885
	back.data.distance = 40
	back.data.spot_blend = 1
	back.data.spot_size = 0.785398
	print ("Function =", "scene_three_point_lighting_beam_3d")
	
##################
#### SCENE, FOUR POINT LIGHTING FUNCTIONS ####
	
def studio_four_point_lighting():
	
	studio_world_settings()
	
	bpy.ops.object.lamp_add(type='SPOT',view_align=False,
		location=(-1.37924830661017, -6.787240982055664, 12.466023445129395), 
		rotation=(-0.27631163597106934, -0.43347325921058655, 1.7720673084259033))
	
	bpy.ops.object.lamp_add(type='SPOT',view_align=False,
		location=(0.0, 2.89731502532959, 13.485641479492188), 
		rotation=(-0.0845556692481041, -6.121555328369141, 1.1120541095733643))
	
	bpy.ops.object.lamp_add(type='SPOT',view_align=False,
		location=(1.2730222940444946, -0.4670710563659668, 16.19774627685547), 
		rotation=(0.16847357153892517, 0.00713651767000556, -4.911602973937988))
	
	bpy.ops.object.lamp_add(type='SPOT',view_align=False,
		location=(0, 0, 0), 
		rotation=(0.16847357153892517, 0.00713651767000556, -4.911602973937988))
		
	key = bpy.data.objects.get('Spot')
	key.name = 'FOUR_POINT_KEY'
	key.data.energy = 10
	key.data.spot_blend = 0.710
	key.data.spot_size = 0.733038
	
	fill = bpy.data.objects.get('Spot.001')
	fill.name = 'FOUR_POINT_FILL'
	fill.data.energy = 3.170
	fill.data.distance = 27.260
	fill.data.spot_blend = 0.899
	fill.data.spot_size = 0.471239

	back = bpy.data.objects.get('Spot.002')
	back.name = 'FOUR_POINT_BACK_01'
	back.data.energy = 6.885
	back.data.distance = 40
	back.data.spot_blend = 1
	back.data.spot_size = 0.785398
	
	back2 = bpy.data.objects.get('Spot.003')
	back2.name = 'FOUR_POINT_BACK_02'
	back2.data.energy = 6.885
	back2.data.distance = 40
	back2.data.spot_blend = 1
	back2.data.spot_size = 0.785398
	print ("Function =", "scene_four_point_lighting")
	
##################
# LIGTHING EFFECT   
def studio_four_point_lighting_effect():
	
	studio_world_settings()
	
	bpy.ops.object.lamp_add(type='SPOT',view_align=False,
		location=(-1.37924830661017, -6.787240982055664, 12.466023445129395), 
		rotation=(-0.27631163597106934, -0.43347325921058655, 1.7720673084259033))
	
	bpy.ops.object.lamp_add(type='SPOT',view_align=False,
		location=(0.0, 2.89731502532959, 13.485641479492188), 
		rotation=(-0.0845556692481041, -6.121555328369141, 1.1120541095733643))
	
	bpy.ops.object.lamp_add(type='SPOT',view_align=False,
		location=(1.2730222940444946, -0.4670710563659668, 16.19774627685547), 
		rotation=(0.16847357153892517, 0.00713651767000556, -4.911602973937988))
	
	bpy.ops.object.lamp_add(type='SPOT',view_align=False,
		location=(1.2730222940444946, -0.4670710563659668, 16.19774627685547), 
		rotation=(0.16847357153892517, 0.00713651767000556, -4.911602973937988))
	
	key = bpy.data.objects.get('Spot')
	key.name = 'FOUR_POINT_KEY'
	key.data.energy = 10
	key.data.spot_blend = 0.710
	key.data.spot_size = 0.733038
	
	fill = bpy.data.objects.get('Spot.001')
	fill.name = 'FOUR_POINT_FILL'
	fill.data.energy = 3.170
	fill.data.distance = 27.260
	fill.data.spot_blend = 0.899
	fill.data.spot_size = 0.471239
	
	back = bpy.data.objects.get('Spot.002')
	back.name = 'FOUR_POINT_BACK_01'
	back.data.energy = 6.885
	back.data.distance = 40
	back.data.spot_blend = 1
	back.data.spot_size = 0.785398
	
	back2 = bpy.data.objects.get('Spot.003')
	back2.name = 'FOUR_POINT_BACK_02'
	back2.data.energy = 6.885
	back2.data.distance = 40
	back2.data.spot_blend = 1
	back2.data.spot_size = 0.785398
	print ("Function =", "scene_four_point_lighting_effect")
	
##################
# WATER EFFECT  
def scene_four_point_lighting_water_effect():
	
	studio_world_settings()
	
	bpy.ops.object.lamp_add(type='SPOT',view_align=False,
		location=(-1.37924830661017, -6.787240982055664, 12.466023445129395), 
		rotation=(-0.1697513610124588, -0.4508619010448456, 1.7264331579208374))
	
	bpy.ops.object.lamp_add(type='SPOT',view_align=False,
		location=(8.521602630615234, -5.951590538024902, 13.485641479492188), 
		rotation=(-0.5312091112136841, -5.951590538024902, -1.582659125328064))
	
	bpy.ops.object.lamp_add(type='SPOT',view_align=False,
		location=(-2.717636823654175, 12.648473739624023, 17.64453125), 
		rotation=(0.4667011499404907, 0.48031553626050486, -3.7193543970980225))
	
	bpy.ops.object.lamp_add(type='SPOT',view_align=False,
		location=(9.084490776062012, 15.511934280395508, 6.869918346405029), 
		rotation=(0.9184449315071106, 0.7577983140945435, -4.486191749572754))
	
	key = bpy.data.objects.get('Spot')
	key.name = 'FOUR_POINT_KEY'
	key.data.energy = 3.973
	key.data.distance = 45
	key.data.spot_blend = 0.710
	key.data.spot_size = 0.872665
	
	fill = bpy.data.objects.get('Spot.001')
	fill.name = 'FOUR_POINT_FILL'
	fill.data.energy = 0.457
	fill.data.distance = 27.260
	fill.data.spot_blend = 0.899
	fill.data.spot_size = 0.471239
	
	back = bpy.data.objects.get('Spot.002')
	back.name = 'FOUR_POINT_BACK_01'
	back.data.energy = 0.578
	back.data.distance = 40
	back.data.spot_blend = 1
	back.data.spot_size = 0.266893
	
	back2 = bpy.data.objects.get('Spot.003')
	back2.name = 'FOUR_POINT_BACK_02'
	back2.data.energy = 0.785
	back2.data.distance = 40
	back2.data.spot_blend = 1
	back2.data.spot_size = 0.785398
	
	if not "WaterTex" in bpy.data.textures:
		import os
		realpath = os.path.expanduser('~/My Documents/blender mess about/water_tex.png')
		try:
			img = bpy.data.images.load(realpath)
		except:
			raise NameError("Cannot load image %s" % realpath)
	
		# Create image texture from image
		cTex = bpy.data.textures.new('WaterTex', type='IMAGE')
		cTex.image = img
		cTex.use_alpha = False
		cTex.use_mipmap_gauss = True
		cTex.filter_type = 'AREA'
		cTex.filter_eccentricity = 1
		cTex.filter_size = 1.37
		cTex.use_filter_size_min = True
		water = bpy.data.textures.get("WaterTex") 
		key.data.active_texture = water
	else:   
		water = bpy.data.textures.get("WaterTex") 
		key.data.active_texture = water
	
	print ("Function =", "scene_four_point_lighting_water_effect")
	
##################
# LASER SHOW
def scene_four_point_lighting_laser_show():
	
	studio_world_settings()
	
	bpy.ops.object.lamp_add(type='SPOT',view_align=False,
		location=(-1.37924830661017, -6.787240982055664, 12.466023445129395),
		rotation=(-0.27631163597106934, -0.43347325921058655, 1.7720673084259033))
	
	bpy.ops.object.lamp_add(type='SPOT',view_align=False,
		location=(0.0, 2.89731502532959, 13.485641479492188),
		rotation=(-0.0845556692481041, -6.121555328369141, 1.1120541095733643))
	
	bpy.ops.object.lamp_add(type='SPOT',view_align=False,
		location=(1.2730222940444946, -0.4670710563659668, 16.19774627685547),
		rotation=(0.16847357153892517, 0.00713651767000556, -4.911602973937988))
	
	bpy.ops.object.lamp_add(type='SPOT',view_align=False,
		location=(1.2730222940444946, -0.4670710563659668, 16.19774627685547),
		rotation=(0.16847357153892517, 0.00713651767000556, -4.911602973937988))
	
	key = bpy.data.objects.get('Spot')
	key.name = 'FOUR_POINT_KEY'
	key.data.energy = 10
	key.data.spot_blend = 0.710
	key.data.spot_size = 0.733038
	
	fill = bpy.data.objects.get('Spot.001')
	fill.name = 'FOUR_POINT_FILL'
	fill.data.energy = 3.170
	fill.data.distance = 27.260
	fill.data.spot_blend = 0.899
	fill.data.spot_size = 0.471239
	
	back = bpy.data.objects.get('Spot.002')
	back.name = 'FOUR_POINT_BACK_01'
	back.data.energy = 6.885
	back.data.distance = 40
	back.data.spot_blend = 1
	back.data.spot_size = 0.785398
	
	back2 = bpy.data.objects.get('Spot.003')
	back2.name = 'FOUR_POINT_BACK_02'
	back2.data.energy = 6.885
	back2.data.distance = 40
	back2.data.spot_blend = 1
	back2.data.spot_size = 0.785398
	
	print ("Function =", "scene_four_point_lighting_laser_show")
	
	
	
	
##################
# SEAMLESS  
def scene_four_point_lighting_seamless():
	
	studio_world_settings()
	
	bpy.ops.object.lamp_add(type='SPOT',view_align=False,
		location=(-1.37924830661017, -6.787240982055664, 12.466023445129395),
		rotation=(-0.27631163597106934, -0.43347325921058655, 1.7720673084259033))
	
	bpy.ops.object.lamp_add(type='SPOT',view_align=False,
		location=(0.0, 2.89731502532959, 13.485641479492188),
		rotation=(-0.0845556692481041, -6.121555328369141, 1.1120541095733643))
	
	bpy.ops.object.lamp_add(type='SPOT',view_align=False,
		location=(1.2730222940444946, -0.4670710563659668, 16.19774627685547),
		rotation=(0.16847357153892517, 0.00713651767000556, -4.911602973937988))
	
	bpy.ops.object.lamp_add(type='SPOT',view_align=False,
		location=(1.2730222940444946, -0.4670710563659668, 16.19774627685547),
		rotation=(0.16847357153892517, 0.00713651767000556, -4.911602973937988))
	
	key = bpy.data.objects.get('Spot')
	key.name = 'FOUR_POINT_KEY'
	key.data.energy = 10
	key.data.spot_blend = 0.710
	key.data.spot_size = 0.733038
	
	fill = bpy.data.objects.get('Spot.001')
	fill.name = 'FOUR_POINT_FILL'
	fill.data.energy = 3.170
	fill.data.distance = 27.260
	fill.data.spot_blend = 0.899
	fill.data.spot_size = 0.471239
	
	back = bpy.data.objects.get('Spot.002')
	back.name = 'FOUR_POINT_BACK_01'
	back.data.energy = 6.885
	back.data.distance = 40
	back.data.spot_blend = 1
	back.data.spot_size = 0.785398
	
	back2 = bpy.data.objects.get('Spot.003')
	back2.name = 'FOUR_POINT_BACK_02'
	back2.data.energy = 6.885
	back2.data.distance = 40
	back2.data.spot_blend = 1
	back2.data.spot_size = 0.785398
	
	print ("Function =", "scene_four_point_lighting_seamless")
	
##################
# LIGHT CONE
def scene_four_point_lighting_light_cone():
	
	studio_world_settings()
	
	bpy.ops.object.lamp_add(type='SPOT',view_align=False,
		location=(-1.37924830661017, -6.787240982055664, 12.466023445129395),
		rotation=(-0.27631163597106934, -0.43347325921058655, 1.7720673084259033))
		
	bpy.ops.object.lamp_add(type='SPOT',view_align=False,
		location=(0.0, 2.89731502532959, 13.485641479492188),
		rotation=(-0.0845556692481041, -6.121555328369141, 1.1120541095733643))
	
	bpy.ops.object.lamp_add(type='SPOT',view_align=False,
		location=(1.2730222940444946, -0.4670710563659668, 16.19774627685547),
		rotation=(0.16847357153892517, 0.00713651767000556, -4.911602973937988))
	
	bpy.ops.object.lamp_add(type='SPOT',view_align=False,
		location=(1.2730222940444946, -0.4670710563659668, 16.19774627685547),
		rotation=(0.16847357153892517, 0.00713651767000556, -4.911602973937988))
	
	key = bpy.data.objects.get('Spot')
	key.name = 'FOUR_POINT_KEY'
	key.data.energy = 10
	key.data.spot_blend = 0.710
	key.data.spot_size = 0.733038
	
	fill = bpy.data.objects.get('Spot.001')
	fill.name = 'FOUR_POINT_FILL'
	fill.data.energy = 3.170
	fill.data.distance = 27.260
	fill.data.spot_blend = 0.899
	fill.data.spot_size = 0.471239
	
	back = bpy.data.objects.get('Spot.002')
	back.name = 'FOUR_POINT_BACK_01'
	back.data.energy = 6.885
	back.data.distance = 40
	back.data.spot_blend = 1
	back.data.spot_size = 0.785398
	
	back2 = bpy.data.objects.get('Spot.003')
	back2.name = 'FOUR_POINT_BACK_02'
	back2.data.energy = 6.885
	back2.data.distance = 40
	back2.data.spot_blend = 1
	back2.data.spot_size = 0.785398
	
	print ("Function =", "scene_four_point_lighting_light_cone")
	
###############################
#### INDOOR LIGHTING FUNCTIONS ####
	
def indoor_day_lighting():
	print ("Function =", "indoor_day_lighting")
	
def indoor_afternoon_lighting():
	print ("Function =", "indoor_afternoon_lighting")
	
def indoor_early_morning_lighting():
	print ("Function =", "indoor_early_morning_lighting")
	
def indoor_day_with_lights_on():
	print ("Function =", "indoor_day_with_lights_on")
	
def indoor_day_overcast_lighting():
	print ("Function =", "indoor_day_overcast_lighting")
	
def indoor_sunset_lighting():
	print ("function = ","indoor_sunset_lighting")
	
def indoor_fake_global_illumination():
	print ("Function =", "indoor_fake_global_illumination")
	
def indoor_night_lighting():	
	print ("Function =", "indoor_night_lighting")
	
####
def Addsketchup1operator1():
	
	# Sketchup style render 
	# Erase all material and texture then add a new mat   white
	# find how many mesh objects in scene 
	
	jj=0
	
	for ob in bpy.data.objects:
	
		if ob.type == 'MESH':
			bpy.context.scene.objects.active = ob
			jj+=1
	
	jj=0
	
	for ob in bpy.data.objects:
	
		if ob.type == 'MESH':
	
			bpy.context.scene.objects.active =ob
			obj_act = bpy.context.active_object 
	
			for x1 in ob.material_slots:
				bpy.ops.object.material_slot_remove()
	
		jj+=1
	
	# Create and Add a new white mat to all objects
	white = makeMaterial('white', (1,1,1), (1,1,1), 1)
	
	# Add mat to all mesh objects
	jj=0
	
	for ob in bpy.data.objects:
	
		if ob.type == 'MESH':
	
			print ()
	
			bpy.context.scene.objects.active =ob
			obj_act = bpy.context.active_object 
	
			setMaterial(bpy.context.object, white)
	
		jj+=1
	
	# Render settings
	wo = bpy.context.scene.render
	wo.use_edge_enhance = True
	
	wo.edge_color = 0,0,0
	wo.edge_threshold = 100
	
	# Set world to AO
	wo = bpy.context.scene.world
	wo.light_settings.use_ambient_occlusion =  True 
	bpy.context.scene.world.light_settings.ao_factor=1.0
	
	
	# Auto camera set up
	global layers, lightboxtype
	global minx, miny, minz, maxx, maxy, maxz, energymult
	
	
	minlistx=[]
	maxlistx=[]
	minlisty=[]
	maxlisty=[]
	minlistz=[]
	maxlistz=[]
	
	maxlistxz=[]
	minlistxz=[]
	
	print (' addlightbox  1 '  )
	
	for ob in bpy.context.scene.objects[:]:
	
		if ob.type!="CAMERA" and ob.type!="EMPTY" and ob.type!="LAMP":
	
			print ()
			print ('ob name=',ob.name,'obtype=',ob.type)
	
			bounds = functions.getobjectBounds(ob)
	
			oxmin = bounds[0][0]
			oxmax = bounds[1][0]
	
			oymin = bounds[0][1]
			oymax = bounds[1][1]
	
			ozmin = bounds[0][2]
			ozmax = bounds[1][2]
	
			print ('bound  oxmin=',oxmin , ' oymin=',oymin  ,'  ozmin=',ozmin)
			print ('bound  oxmax=',oxmax , ' oymax=',oymax  ,'  ozmax=',ozmax)
	
			if oxmin <= minx:
				minx = oxmin
			if oymin <= miny:
				miny = oymin
			if ozmin <= minz:
				minz = ozmin
	
			if oxmax >= maxx:
				maxx = oxmax
			if oymax >= maxy:
				maxy = oymax
			if ozmax >= maxz:
				maxz = ozmax
	
			print (' minx=',minx , ' miny=',miny  ,' minz=',minz)
			print ()
			print (' maxx=',maxx , ' maxy=',maxy  ,' maxz=',maxz)
	
			minlistx.append(oxmin)
			maxlistx.append(oxmax)
			minlisty.append(oymin)
			maxlisty.append(oymax)
			minlistz.append(ozmin)
			maxlistz.append(ozmax)
	
			maxlistxz.append(ozmax)
			maxlistxz.append(oxmax)
	
			minlistxz.append(ozmax)
			minlistxz.append(oxmax)
	
	print ()
	print ('^^^^^^^^^')
	print ()
	
	minx1=min(minlistx)
	maxx1=max(maxlistx)
	
	
	miny1=min(minlisty)
	maxy1=max(maxlisty)
	
	minz1=min(minlistz)
	maxz1=max(maxlistz)
	
	xzmax=max(maxlistxz)   #  determine the max for X and Z  front view and cube scene size in X = size in Z
	xzmin=min(minlistxz)   #  determine the max for X and Z  front view and cube scene size in X = size in Z
	
	scenewx=maxx1-minx1
	scenewy=maxy1-miny1
	scenewz=maxz1-minz1
	
	scenewidth=maxx1-minx1
	
	print ()
	print (' ^^^^^^^^^^^^^^^^^^^^^^ ')
	print (' from list   minx1=',minx1  , ' miny1=',miny1 ,' minz1=',minz1)
	print (' from list   maxx1=',maxx1  , ' maxy1=',maxy1 ,' maxz1=',maxz1)
	print (' from list   scenewx=',scenewx  , ' scenewy=',scenewy ,' scenewz=',scenewz)
	print ()
	print (' from list   max X z =',xzmax ,'min   X z =',xzmin )
	print (' %%%%%%%%%%%    scene front width =',scenewidth)
	print ()
	print (' len list =',len(minlistx))
	
	print ('^^^^^^^^^^^^^^^^^^^^^')
	print ()
	
	midx1 = ((minx1+1) + (maxx1-1)) /2.0
	midy1 = ((miny1+1) + (maxy1-1)) /2.0
	midz1 = ((minz1+1) + (maxz1-1)) /2.0
	
	
	print (' midx1=',midx1, ' midy1=',midy1,' midz1=',midz1)
	
	# Determine size  of camera distance function of max ZX  plane front plane

	bpy.context.scene.objects.active = bpy.context.scene.objects["Camera"]
	print ('Active ob  =',bpy.context.scene.objects.active)
	ob=bpy.context.scene.objects.active
	print ('Active ob  =',ob,'  ob name =',ob.name)
	print ('camera loc =',ob.location)
	print ()
	
	cam = ob.data
	cam.name = 'MyCam'
	print (' cam.lens_unit =',cam.lens_unit)
	print (' cam.type =',cam.type)
	print (' cam.lens =',cam.lens)
	cam.lens_unit = 'DEGREES'
	cam.lens=45
	camdeg=cam.angle
	halfcamdeg=camdeg/2.0
	
	print ('*******************')
	print ('Cam deg field of view =',cam.lens,' millimeters cam angle =',cam.angle,'read  =',degrees(cam.angle),' deg')
	print ()
	
	scenehalfwidth=(scenewidth/2.0)
	scenehalfwidth=(scenewidth*0.8)
	
	hyp1=scenehalfwidth/(sin(halfcamdeg))
	
	print (' 1/2 cam angle =',degrees(halfcamdeg),' Deg')
	print (' Hyp  =',hyp1,' 1/2 scene widht  x =',scenehalfwidth)
	dist1=hyp1*cos(halfcamdeg)
	ob.location.y=(-dist1+miny1)
	print ('miny =',miny1)
	print ('cam dist in front of scene =',dist1,' Cam loc  y =',ob.location.y)
	
####
#### OUTDOOR LIGHTING FUNCTIONS ####
def outdoor_sunrise_lighting():
	world = bpy.context.scene.world
	world.name = 'sunrise'
	world.use_sky_paper = False
	world.use_sky_blend = False
	world.use_sky_real = False
	world.horizon_color = (0.061,0.305,0.444)
	world.zenith_color = (0,0,0)
	world.ambient_color = (0,0,0)
	
	print ("Function =", "outdoor_sunrise_lighting")
	
##################
def outdoor_early_morning_lighting():
	world = bpy.context.scene.world
	world.name = 'morning'
	world.use_sky_paper = False
	world.use_sky_blend = False
	world.use_sky_real = False
	world.horizon_color = (0.061,0.305,0.444)
	world.zenith_color = (0,0,0)
	world.ambient_color = (0,0,0)
	
	print ("Function =", "outdoor_early_morning_lighting")
	
##################
def outdoor_midday_lighting():
	world = bpy.context.scene.world
	world.name = 'mid-day'
	world.use_sky_paper = False
	world.use_sky_blend = False
	world.use_sky_real = False
	world.horizon_color = (0.061,0.305,0.444)
	world.zenith_color = (0,0,0)
	world.ambient_color = (0,0,0)
	
	print ("Function =", "outdoor_midday_lighting")
	
##################
def outdoor_evening_lighting():
	print ("Function =", "outdoor_evening_lighting")
	
def outdoor_sunset_lighting():
	world = bpy.context.scene.world
	world.name = 'Sunset'
	world.use_sky_paper = False
	world.use_sky_blend = True
	world.use_sky_real = False
	world.horizon_color = (0.0,0.051,0.444)
	world.zenith_color = (0,0.005,0.015)
	world.ambient_color = (0,0,0)
	
	print ("Function =", "outdoor_sunset_lighting")
	
##################
def outdoor_day_moon_lighting():
	print ("Function =", "outdoor_day_moon_lighting")
	
	
##################
def outdoor_quarter_moon_lighting():
	
	world = bpy.context.scene.world
	world.name = 'night'
	world.use_sky_paper = False
	world.use_sky_blend = False
	world.use_sky_real = False
	world.horizon_color = (0.0,0.0,0.0)
	world.zenith_color = (0,0,0)
	world.ambient_color = (0,0,0)
	
	print ("Function =", "outdoor_quarter_moon_lighting")
	
	
##################
def outdoor_half_moon_lighting():
	
	world = bpy.context.scene.world
	world.name = 'night'
	world.use_sky_paper = False
	world.use_sky_blend = False
	world.use_sky_real = False
	world.horizon_color = (0.0,0.0,0.0)
	world.zenith_color = (0,0,0)
	world.ambient_color = (0,0,0)
	
	print ("Function =", "outdoor_half_moon_lighting")
	
##################
def outdoor_three_quarter_lighting():
	
	world = bpy.context.scene.world
	world.name = 'night'
	world.use_sky_paper = False
	world.use_sky_blend = False
	world.use_sky_real = False
	world.horizon_color = (0.0,0.0,0.0)
	world.zenith_color = (0,0,0)
	world.ambient_color = (0,0,0)
	
	print ("Function =", "outdoor_three_quarter_lighting")
	
##################
def outdoor_full_moom_lighting():
	
	world = bpy.context.scene.world
	world.name = 'night'
	world.use_sky_paper = False
	world.use_sky_blend = False
	world.use_sky_real = False
	world.horizon_color = (0.0,0.0,0.0)
	world.zenith_color = (0,0,0)
	world.ambient_color = (0,0,0)
	
	print ("Function =", "outdoor_full_moom_lighting")
	
##################
def outdoor_night_no_moon():
	
	world = bpy.context.scene.world
	world.name = 'night'
	world.use_sky_paper = False
	world.use_sky_blend = False
	world.use_sky_real = False
	world.horizon_color = (0.0,0.0,0.0)
	world.zenith_color = (0,0,0)
	world.ambient_color = (0,0,0)
	
	print ("Function =", "outdoor_night_no_moon")
	
##################
#		fourthlamp=True
#		add3spotlightsetup1(fourthlamp=true)
#############
	
def add3spotlightsetup1():
	
	global  energyfilllamp,energybacklamp,layers,faceminy
	global minx , miny,minz,maxx,maxy,maxz,energymult
	
	bpy.ops.object.add(type='EMPTY', view_align=False, enter_editmode=False, location=(0.000000, -3.817210, 8.279530), rotation=(0, 0, 0), layers=(layers))
	
	empty1 = bpy.context.object
	empty1.name = 'new_empty'
	
	bpy.ops.object.lamp_add(type='SPOT', view_align=False, location=(19.430519, -20.502472, 7.496113), rotation=(1.614763, 0.709077, 0.853816), layers=(layers))
	lamp1 = bpy.context.object
	
	bpy.ops.object.lamp_add(type='SPOT', view_align=False, location=(-12.848104, 18.574114, 7.496113), rotation=(1.537930, 1.537930, 3.687180), layers=(layers))
	lamp2 = bpy.context.object
	
	bpy.ops.object.lamp_add(type='SPOT', view_align=False, location=(-13.168015, -18.672356, 15.276655), rotation=(0.941318, 0.917498, -1.187617), layers=(layers))
	lamp3 = bpy.context.object
	
	#Place Empty at the center of the scene
	midx = (minx + maxx)/2
	midy = (miny + maxy)/2
	midz = (minz + maxz)/2
	
	empty1.location.x = midx
	empty1.location.y = midy
	empty1.location.z = midz
		
	### Configure Lighting Setup ###
	lamp1.name = 'Backlamp'							# Back Lamp
	lamp2.name = 'Filllamp'							# Fill Lamp
	lamp3.name = 'Keylamp'							# Key Lamp

	#Set Keylamp Location
	lamp3.location.y = miny
	lamp3.location.x = minx
	lamp3.location.z = maxz
	
	#Calculate Keylamp energy
	m = energymult
	keylampD = functions.getDistance(lamp3, empty1)
	keylampE = (keylampD * m)
	
	#Set Backlamp Location
	lamp1.location.y = maxy
	lamp1.location.x = midx
	lamp1.location.z = midz
	
	#Set Backlamp energy
	m = energymult
	backlampD = functions.getDistance(lamp1, empty1)
	backlampE = (backlampD * m)

	#Set Filllamp Location
	lamp2.location.y = miny
	lamp2.location.x = midx
	lamp2.location.z = midz
	
	#Set Filllamp Energy
	m = energymult
	filllampD = functions.getDistance(lamp2, empty1)
	filllampE = (filllampD * m)
		
	#Setup Lamp 1
	lamp1.data.energy = backlampE
	lamp1.data.distance = backlampD
	lamp1.data.spot_size = 3.141593
	lamp1.data.spot_blend = 1
	lamp1.data.shadow_method = 'BUFFER_SHADOW'
	lamp1.data.shadow_buffer_type = 'HALFWAY'
	lamp1.data.shadow_filter_type = 'GAUSS'
	lamp1.data.shadow_buffer_soft = 10
	lamp1.data.shadow_buffer_size = 2048
	lamp1.data.shadow_buffer_bias = 0.100
	lamp1.data.shadow_buffer_samples = 8
	lamp1.data.use_auto_clip_start = True
	lamp1.data.use_auto_clip_end = True
	
	lamp1.data.color=(1.0,1.0,1.0)
	
	#Setup Lamp 2
	lamp2.data.energy = filllampE   
	lamp2.data.distance = filllampD
	lamp2.data.spot_size = 3.141593
	lamp2.data.spot_blend = 1
	lamp2.data.shadow_method = 'BUFFER_SHADOW'
	lamp2.data.shadow_buffer_type = 'HALFWAY'
	lamp2.data.shadow_filter_type = 'GAUSS'
	lamp2.data.shadow_buffer_soft = 5
	lamp2.data.shadow_buffer_size = 2048
	lamp2.data.shadow_buffer_bias = 0.100
	lamp2.data.shadow_buffer_samples = 16
	lamp2.data.use_auto_clip_start = True
	lamp2.data.use_auto_clip_end = True
	
	lamp2.data.color=(1.0,1.0,0.5)  
	
	#Setup Lamp 3
	lamp3.data.distance = keylampD
	lamp3.data.spot_size = 3.141593
	lamp3.data.spot_blend = 1
	lamp3.data.shadow_method = 'BUFFER_SHADOW'
	lamp3.data.shadow_buffer_type = 'HALFWAY'
	lamp3.data.shadow_filter_type = 'GAUSS'
	lamp3.data.shadow_buffer_soft = 20
	lamp3.data.shadow_buffer_size = 2048
	lamp3.data.shadow_buffer_bias = 1
	lamp3.data.shadow_buffer_samples = 16
	lamp3.data.use_auto_clip_start = True
	lamp3.data.use_auto_clip_end = True
	
	lamp3.data.energy = keylampE
	lamp3.data.color=(0.6,0.6,1.0)
	
	#Add Track Constraints
	functions.addTrackToConstraint(lamp3,'AutoTrack',empty1)
	functions.addTrackToConstraint(lamp1,'AutoTrack',empty1)
	functions.addTrackToConstraint(lamp2,'AutoTrack',empty1)
	
#############
def add3arealightsetup1():
	
	global layers
	
	bpy.ops.object.lamp_add(type='AREA', view_align=False, location=(-12.848104, 18.574114, 7.496113), rotation=(1.537930, 0.711540, 3.687180), layers=(layers))
	lamp1 = bpy.context.object
	
	bpy.ops.object.lamp_add(type='AREA', view_align=False, location=(-13.168015, -18.672356, 15.276655), rotation=(0.941318, 0.917498, -1.187617), layers=(layers))  
	lamp2 = bpy.context.object
	
	bpy.ops.object.lamp_add(type='AREA', view_align=False, location=(19.430519, -20.502472, 7.496113), rotation=(1.614763, 0.709077, 0.853816), layers=(layers))   
	lamp3 = bpy.context.object
	
	### Configure Lighting Setup ###
	lamp1.name = 'Area1'
	lamp2.name = 'Key'
	lamp3.name = 'Area2'

	lamp1.data.energy = 3.0
	lamp1.data.distance = 15.0
	lamp1.data.gamma = 1
	lamp1.data.shadow_method = 'RAY_SHADOW'
	lamp2.data.size = 10
	   
	lamp2.data.energy = 1.0
	lamp2.data.distance = 16.0
	lamp2.data.gamma = 1
	lamp2.data.shadow_method = 'RAY_SHADOW'
	lamp2.data.shadow_ray_samples_x = 16
	lamp2.data.size = 5
	
	lamp3.data.energy = 0.6
	lamp3.data.distance = 8.0
	lamp3.data.gamma = 1
	lamp3.data.shadow_method = 'RAY_SHADOW'
	lamp3.data.shadow_ray_samples_x = 16
	lamp3.data.size = 15
		
############
def Addaddhc1():
	
	global layers
	# http://www.blender.org/documentation/250PythonDoc/bpy.ops.object.html?highlight=bpy.ops.object.lamp_add#bpy.ops.object.lamp_add
	
	bpy.ops.object.lamp_add(type='HEMI', view_align=False, location=(-12.848104, 18.574114, 7.496113), rotation=(1.537930, 0.711540, 3.687180), layers=(layers))
	lamp1 = bpy.context.object
	
	
	bpy.ops.object.lamp_add(type='POINT', view_align=False, location=(-5.0, 7.0, 5.0), rotation=(1.537930, 0.711540, 3.687180), layers=(layers))
	lamp2 = bpy.context.object
	
	### Configure Lighting Setup ###
	lamp1.name = 'emi1'
	lamp2.name = 'point1'


	lamp1.data.energy = 1.0
	lamp1.data.distance = 15.0
	lamp1.data.color=(0.385,0.212,0.212)	#	
	
	
	lamp2.data.energy = 1.0
	lamp2.data.distance = 15.0
	lamp2.data.shadow_method = 'RAY_SHADOW'
	lamp2.data.color=(0.509,0.677,0.851)

	# select and scale the domain :D
	bpy.ops.object.select_pattern(extend=False, pattern="Domain", case_sensitive=False)
	
	if "Domain" in bpy.data.objects:
		bpy.context.active_object.scale = (6.767,6.767,6.767)   
	
############
def Addaddhc2():
	global layers

	# http://www.blender.org/documentation/250PythonDoc/bpy.ops.object.html?highlight=bpy.ops.object.lamp_add#bpy.ops.object.lamp_add
	bpy.ops.object.lamp_add(type='HEMI', view_align=False, location=(0.0, 0.0, 10.0), rotation=(1.537930, 0.711540, 3.687180), layers=(layers))
	lamp1 = bpy.context.object
	
	
	bpy.ops.object.lamp_add(type='AREA', view_align=False, location=(-5.0, 7.0, 5.0), rotation=(1.537930, 0.711540, 3.687180), layers=(layers))
	lamp2 = bpy.context.object
	
	### Configure Lighting Setup ###
	lamp1.name = 'Hemi1'
	lamp2.name = 'Area1'

	lamp1.data.energy = 0.4
	lamp1.data.distance = 15.0
	lamp1.data.use_specular = False 
	lamp1.data.color=(1.0,1.0,1.0)
	
	lamp2.data.energy = 0.25
	lamp2.data.distance = 15.0
	lamp2.data.shadow_method = 'RAY_SHADOW'
	lamp2.data.shadow_ray_samples_x = 4
	lamp2.data.color=(1.0,1.0,1.0)
	
	# select and scale the domain :D
	bpy.ops.object.select_pattern(extend=False, pattern="Domain", case_sensitive=False)
	
	if "Domain" in bpy.data.objects:
		bpy.context.active_object.scale = (6.767,6.767,6.767)   
	
def sepiarenderscene1():
	
	global layers
	
	bpy.context.scene.use_nodes = True
	tree = bpy.context.scene.node_tree
	
	for n in tree.nodes:
		tree.nodes.remove(n)
	
													# Add nodes
	
	rl = tree.nodes.new('R_LAYERS')						# Input render layer  node
	rl.location = 0,-4
	
	im = tree.nodes.new('IMAGE')					# Image node
	im.location = 0,-4
	hs = tree.nodes.new('HUE_SAT')					# HUE_SAT node
	hs.location = 175,50

	hs.color_hue=0.5
	hs.color_saturation=0.712
	hs.color_value=1.0
	
	rgb = tree.nodes.new('RGB')						# RGB node
	rgb.location = 0,-200
	
	rgb.outputs['RGBA'].default_value[0]=0.8			# R
	rgb.outputs['RGBA'].default_value[1]=0.318			# G
	rgb.outputs['RGBA'].default_value[2]=0.28			# B
	rgb.outputs['RGBA'].default_value[3]=0.5			# Alpha
	
	
	bpy.types.RGBANodeSocket.default_value=(0.4,0,8,0.6,1)   #   RBG  plus intensity
	
	
	mix1 = tree.nodes.new('MIX_RGB')				# MIX_RGB node
	mix1.location = 375,50
	mix1.inputs['Fac'].default_value[0] = 0.4
	
	
	blur = tree.nodes.new('BLUR')					# BLUR node
	blur.location = 525,-4
	
	blur.factor=0.333
	blur.factor_x=2.0
	blur.factor_y=3.0
	blur.filter_type="GAUSS"
	
	
	mix2 = tree.nodes.new('MIX_RGB')				# MIX_RGB node
	mix2.location = 700,167
	mix2.inputs['Fac'].default_value[0] = 0.4
	
	view = tree.nodes.new('VIEWER')					# Viewer node
	view.location = 850,167
	
	comp = tree.nodes.new('COMPOSITE')				# Output node
	comp.location = 950,300
	
									# link nodes
	
	links = tree.links
	link0 = links.new(im.outputs[0],hs.inputs[1])
	link1 = links.new(rgb.outputs[0],mix1.inputs[2])
	link2 = links.new(hs.outputs[0],mix1.inputs[1])
	link3 = links.new(mix1.outputs[0],blur.inputs[0])
	link4 = links.new(mix1.outputs[0],mix2.inputs[1])
	link5 = links.new(blur.outputs[0],mix2.inputs[2])
	link6 = links.new(mix2.outputs[0],view.inputs[0])
	link7 = links.new(mix2.outputs[0],comp.inputs[0])
	
#####
def addlightbox33():					# Light box with 3 or 4 area lights
	
	global layers, lightboxtype
	global minx, miny, minz, maxx, maxy, maxz, energymult
	
	
	minlistx=[]
	maxlistx=[]
	minlisty=[]
	maxlisty=[]
	minlistz=[]
	maxlistz=[]
	
	maxlistxz=[]
	minlistxz=[]
	
	print (' addlightbox  1 '  )
    
    # Calculate Scene Size
	for ob in bpy.context.scene.objects[:]:
	
		if ob.type!="CAMERA" and ob.type!="EMPTY" and ob.type!="LAMP":
	
			print ()
			print ('ob name=',ob.name,'obtype=',ob.type)
	
			bounds = functions.getobjectBounds(ob)
	
			oxmin = bounds[0][0]
			oxmax = bounds[1][0]
	
			oymin = bounds[0][1]
			oymax = bounds[1][1]
	
			ozmin = bounds[0][2]
			ozmax = bounds[1][2]
	
			print ('bound  oxmin=',oxmin , ' oymin=',oymin  ,'  ozmin=',ozmin)
			print ('bound  oxmax=',oxmax , ' oymax=',oymax  ,'  ozmax=',ozmax)
	
			if oxmin <= minx:
				minx = oxmin
			if oymin <= miny:
				miny = oymin
			if ozmin <= minz:
				minz = ozmin
	
			if oxmax >= maxx:
				maxx = oxmax
			if oymax >= maxy:
				maxy = oymax
			if ozmax >= maxz:
				maxz = ozmax

			print (' minx=',minx , ' miny=',miny  ,' minz=',minz)
			print ()
			print (' maxx=',maxx , ' maxy=',maxy  ,' maxz=',maxz)
	
			minlistx.append(oxmin)
			maxlistx.append(oxmax)
			minlisty.append(oymin)
			maxlisty.append(oymax)
			minlistz.append(ozmin)
			maxlistz.append(ozmax)
	
			maxlistxz.append(ozmax)
			maxlistxz.append(oxmax)
	
			minlistxz.append(ozmax)
			minlistxz.append(oxmax)
	
	print ()
	print ('^^^^^^^^^')
	print ()
	
	minx1=min(minlistx)
	maxx1=max(maxlistx)
	
	
	miny1=min(minlisty)
	maxy1=max(maxlisty)
	
	minz1=min(minlistz)
	maxz1=max(maxlistz)
	
	xzmax=max(maxlistxz)   #  determine the max for X and Z  front view and cube scene size in X = size in Z
	xzmin=min(minlistxz)   #  determine the max for X and Z  front view and cube scene size in X = size in Z
	
	scenewx=maxx1-minx1
	scenewy=maxy1-miny1
	scenewz=maxz1-minz1
	
	scenewidth=maxx1-minx1
	
	print ()
	print (' ^^^^^^^^^^^^^^^^^^^^^^ ')
	print (' from list   minx1=',minx1  , ' miny1=',miny1 ,' minz1=',minz1)
	print (' from list   maxx1=',maxx1  , ' maxy1=',maxy1 ,' maxz1=',maxz1)
	print (' from list   scenewx=',scenewx  , ' scenewy=',scenewy ,' scenewz=',scenewz)
	print ()
	print (' from list   max X z =',xzmax ,'min   X z =',xzmin )
	print (' %%%%%%%%%%%    scene front width =',scenewidth)
	print ()
	print (' len list =',len(minlistx))
	
	print ('^^^^^^^^^^^^^^^^^^^^^')
	print ()
	
	midx1 = ((minx1+1) + (maxx1-1)) /2.0
	midy1 = ((miny1+1) + (maxy1-1)) /2.0
	midz1 = ((minz1+1) + (maxz1-1)) /2.0
	
	
	print (' midx1=',midx1, ' midy1=',midy1,' midz1=',midz1)
	
	# Determine size  of camera distance function of max ZX  plane front plane
	bpy.context.scene.objects.active = bpy.context.scene.objects["Camera"]
	print ('Active ob  =',bpy.context.scene.objects.active)
	ob=bpy.context.scene.objects.active
	print ('Active ob  =',ob,'  ob name =',ob.name)
	
	print ('camera loc =',ob.location)
	print ()
	
	cam = ob.data
	cam.name = 'MyCam'
	print (' cam.lens_unit =',cam.lens_unit)
	print (' cam.type =',cam.type)
	print (' cam.lens =',cam.lens)
	cam.lens_unit = 'DEGREES'
	cam.lens=45
	camdeg=cam.angle
	halfcamdeg=camdeg/2.0
	
	print ('*******************')
	print ('Cam deg field of view =',cam.lens,' millimeters cam angle =',cam.angle,'read  =',degrees(cam.angle),' deg')
	print ()
	
	mag=1.5*0.5
	dimboxscalex=scenewx*mag
	dimboxscalez=scenewz*mag
	
	print ('scenewx =',scenewx,'dimboxscalex =',dimboxscalex)
	print ('scenewz =',scenewz,'dimboxscalez =',dimboxscalez)

	
	zxmax1=0
	
	if dimboxscalex >=dimboxscalez:
		zxmax1=dimboxscalex
	else:
		zxmax1=dimboxscalez
	
	print (' dimboxscalex=',dimboxscalex)
	
	print ('miny =',miny1,' zxmax1=',zxmax1,'scenewidth/2.0 =',scenewidth/2.0)
	zxmax1=zxmax1*2.2
	print (' zxmax1=',zxmax1)
	print ('*******************')
	
	scenehalfwidth=(scenewidth/2.0)
	scenehalfwidth=(scenewidth*0.8)
	
	hyp1=scenehalfwidth/(sin(halfcamdeg))
	
	print (' 1/2 cam angle =',degrees(halfcamdeg),' Deg')
	print (' Hyp  =',hyp1,' 1/2 scene widht  x =',scenehalfwidth)
	dist1=hyp1*cos(halfcamdeg)
	ob.location.y=(-dist1+miny1)
	print ('miny =',miny1)
	print ('cam dist in front of scene =',dist1,' Cam loc  y =',ob.location.y)
	
	ob.location.z=midz1
	ob.location.x=midx1 
	
	r1=scenehalfwidth/hyp1
	backw=r1*(dist1+scenewy)
	print ('&&&&&&&&&&&&&&&&&&&&')
	print (' 1/2 x w =',scenehalfwidth,' r1=',r1,' backw=',backw)
	print (' 1/2 new w zxmax1  =',zxmax1)
	dimboxscaley=(scenewy+dist1)*mag
	
	lamph=maxz*0.8
	
	print (' dimboxscalex=',dimboxscalex, ' dimboxscaley=',dimboxscaley, ' dimboxscalez=',dimboxscalez)
	print (' maxx*dimboxscale=',dimboxscalex, ' maxy*dimboxscale=',dimboxscaley, ' maxz*dimboxscale=',dimboxscalez)
	print (' maxy*dimboxscale=',dimboxscaley,'scenewy =',scenewy,'dist1  =',dist1)
	
	bpy.ops.mesh.primitive_cube_add(location=(0,0,0))
	ob = bpy.context.object
	ob.name = 'Softbox'
	me = ob.data
	
	bpy.context.scene.objects.active = bpy.context.scene.objects["Softbox"]
	
	yscale1=1.5
	
	bpy.context.scene.objects.active.scale=(zxmax1,dimboxscaley,zxmax1)
	print ()
	print ('Scale Box =  X Box=',zxmax1, ' Y Box =',dimboxscaley, ' Z box =',zxmax1)
	print ()
	
	bpy.ops.object.origin_clear()													# Clear the object origin.
	bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN')								# Set the object origin, by either moving the data, or set to center of data, or use 3d cursor

	ob.location.y=-dimboxscaley/2.0
	ob.location.z=zxmax1
																					# Change to Editmode
	bpy.ops.object.editmode_toggle()
	bpy.ops.mesh.subdivide( number_cuts=3) 											# Add subdivide  to object
																					# Change to Objectmode
	bpy.ops.object.editmode_toggle()
	
    #	http://www.blender.org/documentation/250PythonDoc/bpy.ops.mesh.html?highlight=subdivide#bpy.ops.mesh.subdivide
	bpy.ops.object.modifier_add(type='SUBSURF')										# Add subsurf modifier to object
	subsurf = bpy.context.object.modifiers['Subsurf']
	subsurf.levels = 1																# Changes Subsurf levels
																					# Applys Subsurf Modifier
	bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Subsurf")
																					# Adds smooth shading
	bpy.ops.object.shade_smooth()
	
	bpy.context.active_object.draw_type = "WIRE"									# Make dome wiremesh in viewport
	bpy.context.active_object.show_wire = True
	
	bpy.ops.object.add(type='EMPTY', view_align=False, enter_editmode=False, location=(midx1, midy1,midz1), rotation=(0, 0, 0), layers=(layers))
	
	empty1 = bpy.context.object
	empty1.name = 'empty1'
	
	print ('empty1 loc =',empty1.location)
	
	bpy.context.scene.objects.active = bpy.context.scene.objects["Empty"]
	ob=bpy.context.scene.objects.active
	ob.location.x=midx1
	ob.location.y=midy1
	ob.location.z=midz1
	
	yl1=miny1+dist1/2.0
	print (' yl1=',yl1,' miny1=',miny1,'dist1  =',dist1)
	
	# Middle front Area light
	bpy.ops.object.lamp_add(type='AREA', view_align=False, location=(0, -yl1, zxmax1*0.8), rotation=(0, 0, 0), layers=(layers))  
	
	lamp1 = bpy.context.object
	
	mult=7
	
	x1=-0.2*maxx1
	y1=-0.5*maxy1
	z1=7
	
	x2=-x1*maxx1
	y2=y1*maxy1
	x3=-x2*maxx1
	y3=y2*maxy1
	
	xl2=zxmax1*(2.00**0.5)/2.0
	
	# Left front Area light
	bpy.ops.object.lamp_add(type='AREA', view_align=False, location=(-xl2, -yl1,zxmax1*0.8), rotation=(0, 0, 0), layers=(layers))  
	lamp2 = bpy.context.object
	
	# Right front Area light
	bpy.ops.object.lamp_add(type='AREA', view_align=False, location=(xl2, -yl1,zxmax1*0.8), rotation=(0, 0, 0), layers=(layers))  
	lamp3 = bpy.context.object
	
	### Configure Lighting Setup ###
	lamp1.name = 'area1'												# Middle front Area light
	lamp2.name = 'area2'												# Left front Area light
	lamp3.name = 'area3'												# Right front Area light
	
	# Set Lamp energy
	m =0.05
	lampD = functions.getDistance(lamp1, empty1)
	lampE = m*(lampD /(lampD*2.0))
	
	addenergy = 1.0
	
	lamp1.data.energy = lampE
	lamp1.data.distance = lampD
	lamp1.data.gamma = 1
	lamp1.data.shadow_method = 'RAY_SHADOW'
	lamp1.data.color=(1.0,1.0,1.0)										# Middle front Area light
	lamp1.data.size = 10
	 
	lampD = functions.getDistance(lamp2, empty1)
	lampE = (lampD * m) *0.5											# Reduce intensity to half
	   
	lamp2.data.energy = lampE
	lamp2.data.distance = lampD
	lamp2.data.gamma = 1
	lamp2.data.shadow_method = 'RAY_SHADOW'
	lamp2.data.color=(1.0,1.0,1.0)										# Left front Area light
	lamp2.data.size = 10
	 
	 
	lampD = functions.getDistance(lamp3, empty1)
	lampE = (lampD * m) *0.5											# Reduce intensity to half
	   
	lamp3.data.energy = lampE
	lamp3.data.distance = lampD
	lamp3.data.gamma = 1
	lamp3.data.shadow_method = 'RAY_SHADOW'
	lamp3.data.color=(1.0,1.0,1.0)										# Right front Area light
	lamp3.data.size = 10
	
	# Add Track Constraints
	functions.addTrackToConstraint(lamp1,'AutoTrack',empty1 )
	functions.addTrackToConstraint(lamp2,'AutoTrack',empty1 )
	functions.addTrackToConstraint(lamp3,'AutoTrack',empty1 )
	
	# Lamp #4
	if lightboxtype:
	
	# Top Area light
		bpy.ops.object.lamp_add(type='AREA', view_align=False, location=(0, 0,zxmax1*1.3), rotation=(0, 0, 0), layers=(layers))  
		lamp4 = bpy.context.object
	
		lamp4.name = 'area4'												# Top Area light
	
		lamp4.data.energy = lampE
		lamp4.data.distance = lampD
		lamp4.data.gamma = 1
		lamp4.data.shadow_method = 'RAY_SHADOW'
		lamp4.data.color=(1.0,1.0,1.0)										# Top Area light
		lamp4.data.size = 10
	
		functions.addTrackToConstraint(lamp4,'AutoTrack',empty1 )
	
	lightboxtype=False

####
def addlightbox34():					# Light box with 3 or 4 area lights
	
	global lightboxtype
	
	lightboxtype=True
	
	addlightbox33()
	
	
####
def addlightbox():
	
	global layers
	global minx, miny, minz, maxx, maxy, maxz, energymult
	
	minlistx=[]
	maxlistx=[]
	minlisty=[]
	maxlisty=[]
	minlistz=[]
	maxlistz=[]
	
	maxlistxz=[]
	minlistxz=[]
	
	print (' addlightbox  1 '  )

	# Calculate Scene Size
	for ob in bpy.context.scene.objects[:]:
	
		if ob.type!="CAMERA" and ob.type!="EMPTY" and ob.type!="LAMP":
	
	
			print ()
			print ('ob name=',ob.name,'obtype=',ob.type)
			bounds = functions.getobjectBounds(ob)

			oxmin = bounds[0][0]
			oxmax = bounds[1][0]
	
			oymin = bounds[0][1]
			oymax = bounds[1][1]
	
			ozmin = bounds[0][2]
			ozmax = bounds[1][2]
	
			print ('bound  oxmin=',oxmin , ' oymin=',oymin  ,'  ozmin=',ozmin)
			print ('bound  oxmax=',oxmax , ' oymax=',oymax  ,'  ozmax=',ozmax)
	
			if oxmin <= minx:
				minx = oxmin
			if oymin <= miny:
				miny = oymin
			if ozmin <= minz:
				minz = ozmin
	
			if oxmax >= maxx:
				maxx = oxmax
			if oymax >= maxy:
				maxy = oymax
			if ozmax >= maxz:
				maxz = ozmax
	
	
			print (' minx=',minx , ' miny=',miny  ,' minz=',minz)
			print ()
			print (' maxx=',maxx , ' maxy=',maxy  ,' maxz=',maxz)
	
			minlistx.append(oxmin)
			maxlistx.append(oxmax)
			minlisty.append(oymin)
			maxlisty.append(oymax)
			minlistz.append(ozmin)
			maxlistz.append(ozmax)
	
			maxlistxz.append(ozmax)
			maxlistxz.append(oxmax)
	
			minlistxz.append(ozmax)
			minlistxz.append(oxmax)
	
	print ()
	print ('^^^^^^^^^')
	print ()
	
	minx1=min(minlistx)
	maxx1=max(maxlistx)
	
	miny1=min(minlisty)
	maxy1=max(maxlisty)
	
	minz1=min(minlistz)
	maxz1=max(maxlistz)
	
	xzmax=max(maxlistxz)   #  determine the max for X and Z  front view and cube scene size in X = size in Z
	xzmin=min(minlistxz)   #  determine the max for X and Z  front view and cube scene size in X = size in Z
	
	scenewx=maxx1-minx1
	scenewy=maxy1-miny1
	scenewz=maxz1-minz1

	scenewidth=maxx1-minx1
	
	print ()
	print (' ^^^^^^^^^^^^^^^^^^^^^^ ')
	print (' from list   minx1=',minx1  , ' miny1=',miny1 ,' minz1=',minz1)
	print (' from list   maxx1=',maxx1  , ' maxy1=',maxy1 ,' maxz1=',maxz1)
	print (' from list   scenewx=',scenewx  , ' scenewy=',scenewy ,' scenewz=',scenewz)
	print ()
	print (' from list   max X z =',xzmax ,'min   X z =',xzmin )
	print (' %%%%%%%%%%%    scene front width =',scenewidth)
	print ()
	print (' len list =',len(minlistx))
	
	print ('^^^^^^^^^^^^^^^^^^^^^')
	print ()
	
	midx1 = ((minx1+1) + (maxx1-1)) /2.0
	midy1 = ((miny1+1) + (maxy1-1)) /2.0
	midz1 = ((minz1+1) + (maxz1-1)) /2.0
	
	print (' midx1=',midx1, ' midy1=',midy1,' midz1=',midz1)
	
	# Determine size  of camera distance function of max ZX  plane front plane
	bpy.context.scene.objects.active = bpy.context.scene.objects["Camera"]
	print ('Active ob  =',bpy.context.scene.objects.active)
	ob=bpy.context.scene.objects.active
	print ('Active ob  =',ob,'  ob name =',ob.name)
	
	print ('camera loc =',ob.location)
	print ()
	
	cam = ob.data
	cam.name = 'MyCam'
	print (' cam.lens_unit =',cam.lens_unit)
	print (' cam.type =',cam.type)
	print (' cam.lens =',cam.lens)
	cam.lens_unit = 'DEGREES'
	cam.lens=45
	camdeg=cam.angle
	halfcamdeg=camdeg/2.0
	
	print ('*******************')
	print ('Cam deg field of view =',cam.lens,' millimeters cam angle =',cam.angle,'read  =',degrees(cam.angle),' deg')
	print ()
	
	mag=1.5*0.5
	dimboxscalex=scenewx*mag
	dimboxscalez=scenewz*mag
	
	print ('scenewx =',scenewx,'dimboxscalex =',dimboxscalex)
	print ('scenewz =',scenewz,'dimboxscalez =',dimboxscalez)
	
	zxmax1=0
	
	if dimboxscalex >=dimboxscalez:
		zxmax1=dimboxscalex
	else:
		zxmax1=dimboxscalez
	
	print (' dimboxscalex=',dimboxscalex)
	
	print ('miny =',miny1,' zxmax1=',zxmax1,'scenewidth/2.0 =',scenewidth/2.0)
	zxmax1=zxmax1*2.2
	print (' zxmax1=',zxmax1)
	print ('*******************')
	
	scenehalfwidth=(scenewidth/2.0)
	scenehalfwidth=(scenewidth*0.8)
	
	hyp1=scenehalfwidth/(sin(halfcamdeg))
	
	
	print (' 1/2 cam angle =',degrees(halfcamdeg),' Deg')
	print (' Hyp  =',hyp1,' 1/2 scene widht  x =',scenehalfwidth)
	dist1=hyp1*cos(halfcamdeg)

	ob.location.y=(-dist1+miny1)
	print ('miny =',miny1)
	print ('cam dist in front of scene =',dist1,' Cam loc  y =',ob.location.y)
	
	ob.location.z=midz1
	ob.location.x=midx1 
	
	r1=scenehalfwidth/hyp1
	backw=r1*(dist1+scenewy)
	print ('&&&&&&&&&&&&&&&&&&&&')
	print (' 1/2 x w =',scenehalfwidth,' r1=',r1,' backw=',backw)
	print (' 1/2 new w zxmax1  =',zxmax1)

	dimboxscaley=(scenewy+dist1)*mag
	
	lamph=maxz*0.8
	
	print (' dimboxscalex=',dimboxscalex, ' dimboxscaley=',dimboxscaley, ' dimboxscalez=',dimboxscalez)
	print (' maxx*dimboxscale=',dimboxscalex, ' maxy*dimboxscale=',dimboxscaley, ' maxz*dimboxscale=',dimboxscalez)
	print (' maxy*dimboxscale=',dimboxscaley,'scenewy =',scenewy,'dist1  =',dist1)
	
	
	bpy.ops.mesh.primitive_cube_add(location=(0,0,0))
	ob = bpy.context.object
	ob.name = 'Softbox'
	me = ob.data
	
	bpy.context.scene.objects.active = bpy.context.scene.objects["Softbox"]
	
	# Scale Y in front of scene to set the camera functin of angle
	yscale1=1.5
	
	bpy.context.scene.objects.active.scale=(zxmax1,dimboxscaley,zxmax1)
	
	bpy.ops.object.origin_clear()													# Clear the objet origin.
	bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN')								# Set the object origin, by either moving the data, or set to center of data, or use 3d cursor
	ob.location.y=-dimboxscaley/2.0
	
	ob.location.z=zxmax1
																					# Change to Editmode
	bpy.ops.object.editmode_toggle()
	bpy.ops.mesh.subdivide( number_cuts=3) 											# Add subdivide  to object
																					# Change to Objectmode
	bpy.ops.object.editmode_toggle()
	
    #	http://www.blender.org/documentation/250PythonDoc/bpy.ops.mesh.html?highlight=subdivide#bpy.ops.mesh.subdivide
	bpy.ops.object.modifier_add(type='SUBSURF')										# Add subsurf modifier to object
	subsurf = bpy.context.object.modifiers['Subsurf']
	subsurf.levels = 1																# Changes Subsurf levels
																					# Applys Subsurf Modifier
	bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Subsurf")
																					# Adds smooth shading
	bpy.ops.object.shade_smooth()
	
	bpy.context.active_object.draw_type = "WIRE"									# Make dome wiremesh in viewport
	bpy.context.active_object.show_wire = True
	
	bpy.ops.object.add(type='EMPTY', view_align=False, enter_editmode=False, location=(midx1, midy1,midz1), rotation=(0, 0, 0), layers=(layers))
	
	empty1 = bpy.context.object
	empty1.name = 'empty1'
	
	print ('empty1 loc =',empty1.location)
	
	bpy.context.scene.objects.active = bpy.context.scene.objects["Empty"]
	ob=bpy.context.scene.objects.active
	ob.location.x=midx1
	ob.location.y=midy1
	ob.location.z=midz1
	
	yl1=miny1+dist1/2.0
	print (' yl1=',yl1,' miny1=',miny1,'dist1  =',dist1)

	# Middle front Area light
	bpy.ops.object.lamp_add(type='AREA', view_align=False, location=(0, -yl1, zxmax1*0.8), rotation=(0, 0, 0), layers=(layers))  
	
	lamp1 = bpy.context.object
	
	mult=7
	
	x1=-0.2*maxx1
	y1=-0.5*maxy1
	z1=7
	
	x2=-x1*maxx1
	y2=y1*maxy1
	x3=-x2*maxx1
	y3=y2*maxy1
	
	xl2=zxmax1*(2.00**0.5)/2.0
	
	# Left front Area light
	bpy.ops.object.lamp_add(type='AREA', view_align=False, location=(-xl2, -yl1,zxmax1*0.8), rotation=(0, 0, 0), layers=(layers))  
	lamp2 = bpy.context.object
	
	# Right front Area light
	bpy.ops.object.lamp_add(type='AREA', view_align=False, location=(xl2, -yl1,zxmax1*0.8), rotation=(0, 0, 0), layers=(layers))  
	
	lamp3 = bpy.context.object
	
	### Configure Lighting Setup ###
	lamp1.name = 'area1'												# Middle front Area light
	lamp2.name = 'area2'												# Left front Area light
	lamp3.name = 'area3'												# Right front Area light

	#Set Lamp energy
	m =0.05
	lampD = functions.getDistance(lamp1, empty1)
	lampE = m*(lampD /(lampD*2.0))
	
	addenergy = 1.0
	
	lamp1.data.energy = lampE
	lamp1.data.distance = lampD
	lamp1.data.gamma = 1
	lamp1.data.shadow_method = 'RAY_SHADOW'
	lamp1.data.color=(1.0,1.0,1.0)										# Middle front Area light
	lamp1.data.size = 10
	 
	lampD = functions.getDistance(lamp2, empty1)
	lampE = (lampD * m) *0.5											# Reduce intensity to half
	   
	lamp2.data.energy = lampE
	lamp2.data.distance = lampD
	lamp2.data.gamma = 1
	lamp2.data.shadow_method = 'RAY_SHADOW'
	lamp2.data.color=(1.0,1.0,1.0)										# Left front Area light
	lamp2.data.size = 10
	 
	 
	lampD = functions.getDistance(lamp3, empty1)
	lampE = (lampD * m) *0.5											# Reduce intensity to half
	   
	lamp3.data.energy = lampE
	lamp3.data.distance = lampD
	lamp3.data.gamma = 1
	lamp3.data.shadow_method = 'RAY_SHADOW'
	lamp3.data.color=(1.0,1.0,1.0)										# Right front Area light
	lamp3.data.size = 10
	
	#Add Track Constraints
	functions.addTrackToConstraint(lamp1,'AutoTrack',empty1 )
	functions.addTrackToConstraint(lamp2,'AutoTrack',empty1 )
	functions.addTrackToConstraint(lamp3,'AutoTrack',empty1 )
	
###############
def addlightbox2():
	
	global layers
	global minx, miny, minz, maxx, maxy, maxz, energymult
	
	scene = bpy.context.scene
	
	minx = minx + 1
	miny = miny + 1
	minz = minz + 1
	
	maxx = maxx - 1
	maxy = maxy - 1
	maxz = maxz - 1
	
	midx = (minx + maxx) /2
	midy = (miny + maxy) /2
	midz = (minz + maxz) /2
	
	print (' minx=',minx, ' miny=',miny,' minz=',minz)
	print (' maxx=',maxx, ' maxy=',maxy,' maxz=',maxz)
	print (' size x=',maxx-minx, ' size y=',maxy+miny,' size z=',maxz+minz)
	print (' midx=',midx, ' midy=',midy,' midz=',midz)
	
	dimboxscale=7
	print ('dimboxscale=',dimboxscale)
	
	lamph=maxz*0.8
	
	bpy.ops.mesh.primitive_cube_add(location=(0,0,0))
	ob = bpy.context.object
	ob.name = 'Softbox'
	me = ob.data
	
	bpy.context.scene.objects.active = bpy.context.scene.objects['Softbox']
	bpy.context.scene.objects.active.scale=(maxx*dimboxscale,maxy*dimboxscale,maxz*dimboxscale)
	
	bpy.ops.object.origin_clear() # Clear the objects origin.
	bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN') # Set the objects origin, by either moving the data, or set to center of data, or use 3d cursor
	ob.location.z=midz
																				# Change to Editmode
	bpy.ops.object.editmode_toggle()
	bpy.ops.mesh.subdivide( number_cuts=3) 										# Add subdivide  to object
																				# Change to Objectmode
	bpy.ops.object.editmode_toggle()
	
    #	http://www.blender.org/documentation/250PythonDoc/bpy.ops.mesh.html?highlight=subdivide#bpy.ops.mesh.subdivide
	bpy.ops.object.modifier_add(type='SUBSURF')								# Add subsurf modifier to object
	subsurf = bpy.context.object.modifiers['Subsurf']
	subsurf.levels = 1														# Changes Subsurf levels
																			# Applys Subsurf Modifier
	bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Subsurf")
	bpy.ops.object.shade_smooth()
	
	bpy.context.active_object.draw_type = "WIRE"				# Make dome wiremesh in viewport
	bpy.context.active_object.show_wire = True
	
	bpy.ops.object.add(type='EMPTY', view_align=False, enter_editmode=False, location=(0, 0,midz), rotation=(0, 0, 0), layers=(layers))
	
	empty1 = bpy.context.object
	empty1.name = 'empty1'
	
	# First Area lamp  in front of the left  with an added  reflection plane
	
	bpy.ops.object.lamp_add(type='AREA', view_align=False, location=(minx, -maxy*0.8, lamph), rotation=(0, 0, 0), layers=(layers))  
	lamp1 = bpy.context.object
	lamp1.name = 'area1'
	
	# Add a reflection plane
	# Object
	bpy.ops.mesh.primitive_plane_add(view_align=False,enter_editmode=False,rotation=(0, 0, 0))
	obj_act = bpy.context.active_object
	obj_act.name="reflect1"
	bpy.context.active_object.scale[0] =1.0
	bpy.context.active_object.scale[1] =1.0
	obj_act.location.z += maxz
	
	#   Parent plane to lamp
	
	print ('obj_act.name  =',obj_act.name)
	
	bpy.ops.object.select_all(action='DESELECT')
	bpy.ops.object.select_pattern(extend=True, pattern="reflect1", case_sensitive=False)
	
	scene.update()
	bpy.ops.object.parent_set(type ='OBJECT') 								# parent
	
	# Second Area lamp  in front of the Right  with an added  reflection plane
	bpy.ops.object.lamp_add(type='AREA', view_align=False, location=(maxx, -maxy*0.8, lamph), rotation=(0, 0, 0), layers=(layers))  
	lamp2 = bpy.context.object
	
	lamp2.name = 'area2'
	
	# Add a reflection plane
	bpy.ops.mesh.primitive_plane_add()
	obj_act = bpy.context.active_object
	obj_act.name="reflect2"
	bpy.context.active_object.scale[0] =1.0
	bpy.context.active_object.scale[1] =1.0
	obj_act.location.z += maxz
	
	#   Parent plane to lamp
	bpy.ops.object.select_all(action='DESELECT')
	bpy.ops.object.select_pattern(extend=True, pattern=obj_act.name, case_sensitive=False)
	
	bpy.ops.object.select_pattern(extend=True, pattern=lamp2.name, case_sensitive=False)
	scene.update()
	print ('  Join    Selected objects =',bpy.context.selected_objects)
	
	bpy.ops.object.parent_set(type ='OBJECT') 								# parent
	
	mult=7
	
	x1=-0.2*maxx
	y1=-0.5*maxy
	z1=7
	
	x2=-x1*maxx
	y2=y1*maxy
	x3=-x2*maxx
	y3=y2*maxy
	
	# Third Area lamp  in middle Back 
	bpy.ops.object.lamp_add(type='AREA', view_align=False, location=(0, maxy, lamph), rotation=(0, 0, 0), layers=(layers))  
	lamp3 = bpy.context.object
	lamp3.name = 'area3'
	
	
	### Configure Lighting Setup ###
	# Fourth  Area lamp  in middle Top
	
	bpy.ops.object.lamp_add(type='AREA', view_align=False, location=(0,0, maxz), rotation=(0, 0, 0), layers=(layers))  
	lamp4 = bpy.context.object
	lamp4.name = 'area4'
	
	lamp4.data.energy = 1.0
	lamp4.data.distance = 15.0
	lamp4.data.gamma = 1
	lamp4.data.shadow_method = 'RAY_SHADOW'
	lamp4.data.color=(1.0,1.0,1.0)											# Area lamp on Top of scene
	lamp4.data.size = 10
	
	#Set Lamp energy
	m =0.1
	lampD = functions.getDistance(lamp1, empty1)
	lampE = (lampD * m)
	
	addenergy = 1.0
	
	lamp1.data.energy = lampE
	lamp1.data.distance = lampD
	lamp1.data.gamma = 1
	lamp1.data.shadow_method = 'RAY_SHADOW'
	lamp1.data.color=(1.0,1.0,1.0)											# Area lamp
	lamp1.data.size = 10
	 
	lampD = functions.getDistance(lamp2, empty1)
	lampE = (lampD * m) 
	   
	lamp2.data.energy = lampE
	lamp2.data.distance = lampD
	lamp2.data.gamma = 1
	lamp2.data.shadow_method = 'RAY_SHADOW'
	lamp2.data.color=(1.0,1.0,1.0)											# Area lamp
	lamp2.data.size = 10
	 
	lampD = functions.getDistance(lamp3, empty1)
	lampE = (lampD * m) 

	lamp2.data.energy = lampE
	lamp2.data.distance = lampD
	lamp3.data.gamma = 1
	lamp3.data.shadow_method = 'RAY_SHADOW'
	lamp3.data.color=(1.0,1.0,1.0)											# Area lamp
	lamp3.data.size = 10
	
	#Add Track Constraints
	
	functions.addTrackToConstraint(lamp1,'AutoTrack',empty1 )
	functions.addTrackToConstraint(lamp2,'AutoTrack',empty1 )
	functions.addTrackToConstraint(lamp3,'AutoTrack',empty1 )
	functions.addTrackToConstraint(lamp4,'AutoTrack',empty1 )
	
###############
def Add_fakeaocirclelight16():
	
	global layers
	global minx , miny,minz,maxx,maxy,maxz,energymult

	#Place Empty at the center of the scene
	minx = minx + 1
	miny = miny + 1
	minz = minz + 1
	
	maxx = maxx - 1
	maxy = maxy - 1
	maxz = maxz - 1
	
	midx = (minx + maxx) /2
	midy = (miny + maxy) /2
	midz = (minz + maxz) /2
	
	nlamp=16
	rad1=10
	delang=360.0/nlamp
	height1=maxz*2.0
	
	for i1 in range(0,nlamp):											# Add number of lamps
	
		an1=delang*i1
		locx=rad1*cos(radians(an1))
		locy=rad1*sin(radians(an1))
		locz=height1
	
		bpy.ops.object.lamp_add(type='POINT', view_align=False, location=(locx, locy, locz), rotation=(0, 0, 0), layers=(layers))
		lamp1 = bpy.context.object
		lamp1.data.energy = 1.0
		lamp1.data.distance = 15.0
		lamp1.data.shadow_method = 'RAY_SHADOW'
		lamp1.data.color=(1.0,1.0,1.0)
	
	bpy.ops.object.select_pattern(extend=False, pattern="Empty", case_sensitive=False)
	key1 = bpy.context.object
	bpy.ops.object.select_pattern(extend=False, pattern="Point", case_sensitive=False)
	key = bpy.context.object
	
	bpy.ops.object.select_by_type(extend=False, type='LAMP')
	bpy.ops.object.make_links_data(type='OBDATA')
	
	#Set Lamp energy
	m = .9
	
	lampD = functions.getDistance(key, key1)
	lampE = (lampD * m)/nlamp
	
	lamp1.data.energy = lampE
	lamp1.data.distance =lampD
	
	bpy.ops.object.select_all(action='DESELECT')
	
	print ('16 lamps energie =',lampE,' dist=',lampD )
	
############
def Addaoindirect1():
	
	global  energyfilllamp,energybacklamp,layers,faceminy

	# http://www.blender.org/documentation/250PythonDoc/bpy.ops.object.html?highlight=bpy.ops.object.lamp_add#bpy.ops.object.lamp_add
	defaultworld1()								# Reset to default world settings
	
	wo = bpy.context.scene.world
	wo.light_settings.use_ambient_occlusion =  True 
	bpy.context.scene.world.light_settings.ao_factor=0.3
	
	wo.light_settings.use_environment_light =True
	bpy.context.scene.world.light_settings.environment_energy=0.25
	
	print ('  %%%%%%%%%%%%%%%    Executing the AAO Indirect  function here')
	
############
def Addao1():
	
	global  energyfilllamp,energybacklamp,layers,faceminy
	global minx , miny,minz,maxx,maxy,maxz,energymult
	
	# http://www.blender.org/documentation/250PythonDoc/bpy.ops.object.html?highlight=bpy.ops.object.lamp_add#bpy.ops.object.lamp_add
	defaultworld1()								# Reset to default world settings
	
	wo = bpy.context.scene.world
	wo.light_settings.use_ambient_occlusion =  True
	wo.light_settings.gather_method = "RAYTRACE"  
	bpy.context.scene.world.light_settings.ao_factor=0.5
	
	print ('  %%%%%%%%%%%%%%%    Executing the AO  function here')
	
	bpy.ops.object.add(type='EMPTY', view_align=False, enter_editmode=False, location=(0.000000, -3.817210, 8.279530), rotation=(0, 0, 0), layers=(layers))
	
	empty1 = bpy.context.object
	empty1.name = 'new_empty'
	
	bpy.ops.object.lamp_add(type='SPOT', view_align=False, location=(19.430519, -20.502472, 7.496113), rotation=(1.614763, 0.709077, 0.853816), layers=(layers))
	lamp1 = bpy.context.object
	
	#Place Empty at the center of the scene
	midx = (minx + maxx)/2
	midy = (miny + maxy)/2
	midz = (minz + maxz)/2
	
	empty1.location.x = midx
	empty1.location.y = midy
	empty1.location.z = midz
		
	### Configure Lighting Setup ###
	lamp1.name = 'volumespot1'						  # Spot Lamp with volume

	lamp1.data.energy = 4.0
	lamp1.data.distance = 25.0
	lamp1.data.spot_size = 1.396264
	lamp1.data.spot_blend = 1
	lamp1.data.shadow_method = 'BUFFER_SHADOW'
	lamp1.data.shadow_buffer_type = 'HALFWAY'
	lamp1.data.shadow_filter_type = 'GAUSS'
	lamp1.data.shadow_buffer_soft = 10
	lamp1.data.shadow_buffer_size = 2048
	lamp1.data.shadow_buffer_bias = 0.100
	lamp1.data.shadow_buffer_samples = 8
	lamp1.data.use_auto_clip_start = True
	lamp1.data.use_auto_clip_end = True
	
	#Add Track Constraints
	functions.addTrackToConstraint(lamp1,'AutoTrack',empty1)
	
############
def Addaao1():
	
	
	global  energyfilllamp,energybacklamp,layers,faceminy
	global minx , miny,minz,maxx,maxy,maxz,energymult
	
	
	# http://www.blender.org/documentation/250PythonDoc/bpy.ops.object.html?highlight=bpy.ops.object.lamp_add#bpy.ops.object.lamp_add
	defaultworld1()								# Reset to default world settings
	
	wo = bpy.context.scene.world
	wo.light_settings.use_ambient_occlusion =  True
	wo.light_settings.gather_method = "APPROXIMATE" 
	bpy.context.scene.world.light_settings.ao_factor=0.5
	
	print ('  %%%%%%%%%%%%%%%    Executing the AAO  function here')
	
	bpy.ops.object.add(type='EMPTY', view_align=False, enter_editmode=False, location=(0.000000, -3.817210, 8.279530), rotation=(0, 0, 0), layers=(layers))
	
	empty1 = bpy.context.object
	empty1.name = 'new_empty'
	
	bpy.ops.object.lamp_add(type='SPOT', view_align=False, location=(19.430519, -20.502472, 7.496113), rotation=(1.614763, 0.709077, 0.853816), layers=(layers))
	lamp1 = bpy.context.object
	
	#Place Empty at the center of the scene
	midx = (minx + maxx)/2
	midy = (miny + maxy)/2
	midz = (minz + maxz)/2
	
	empty1.location.x = midx
	empty1.location.y = midy
	empty1.location.z = midz
		
	### Configure Lighting Setup ###
	lamp1.name = 'volumespot1'						  # Spot Lamp with volume

	lamp1.data.energy = 4.0
	lamp1.data.distance = 25.0
	lamp1.data.spot_size = 1.396264
	lamp1.data.spot_blend = 1
	lamp1.data.shadow_method = 'BUFFER_SHADOW'
	lamp1.data.shadow_buffer_type = 'HALFWAY'
	lamp1.data.shadow_filter_type = 'GAUSS'
	lamp1.data.shadow_buffer_soft = 10
	lamp1.data.shadow_buffer_size = 2048
	lamp1.data.shadow_buffer_bias = 0.100
	lamp1.data.shadow_buffer_samples = 8
	lamp1.data.use_auto_clip_start = True
	lamp1.data.use_auto_clip_end = True
	
	#Add Track Constraints
	functions.addTrackToConstraint(lamp1,'AutoTrack',empty1)
	
############
def Addenvironment1():

	global layers

	# http://www.blender.org/documentation/250PythonDoc/bpy.ops.object.html?highlight=bpy.ops.object.lamp_add#bpy.ops.object.lamp_add
	defaultworld1()											# Reset to default world settings
	
	wo = bpy.context.scene.world
	bpy.context.scene.world.light_settings.use_environment_light =True
	bpy.context.scene.world.light_settings.environment_energy=0.5
	
	print ('  %%%%%%%%%%%%%%%    Executing the indirect  function here')
	
############
def Addindirect1():
	
	
	global layers
	
	# http://www.blender.org/documentation/250PythonDoc/bpy.ops.object.html?highlight=bpy.ops.object.lamp_add#bpy.ops.object.lamp_add
	bpy.ops.object.lamp_add(type='HEMI', view_align=False, location=(0.0, 0.0, 10.0), rotation=(1.537930, 0.711540, 3.687180), layers=(layers))
	lamp1 = bpy.context.object
	
	wo = bpy.context.scene.world
	wo.light_settings.use_indirect_light = True 
	bpy.context.scene.world.light_settings.use_indirect_light=True
	bpy.context.scene.world.light_settings.indirect_factor=1.1
	
	print ('  %%%%%%%%%%%%%%%    Executing the indirect  function here')
	
#############
def defaultworld1():
	
	# Reset World to Default manufacture values
	wo = bpy.context.scene.world
	
	wo.use_sky_paper=False
	wo.use_sky_blend=False
	wo.use_sky_real=False
	
	wo.horizon_color=(0.051,)*3						# or =(0.051, 0.051, 0.051)
	wo.zenith_color=(0.010,)*3
	wo.ambient_color=(0.0,)*3  
	
	wo.light_settings.use_ambient_occlusion = False 
	wo.light_settings.use_environment_light =False
	wo.light_settings.use_indirect_light = False 
	
	wo.mist_settings.use_mist = False
	wo.star_settings.use_stars = False
	
	bpy.context.scene.world.texture_slots.clear(0)
	bpy.context.scene.world.texture_slots.clear(1)
	bpy.context.scene.world.texture_slots.clear(2)
	bpy.context.scene.world.texture_slots.clear(3)
	bpy.context.scene.world.texture_slots.clear(4)
	
#############
def clayrender1():
	
	import bpy
	import os 
	from bpy.props import BoolProperty
	 
	 
	bpy.types.Scene.Clay = BoolProperty(
		name="Active Clay", 
		description="Use Clay Render")
	bpy.context.scene.Clay  = False
	
	def search():
		mats = bpy.data.materials
		Find = False
		id = None 
		for m in mats:
			if m.name == "Clay_Render":
				id = m
				Find = True
				break
		return id
	 
	def create_mat():
		id = search()
		if id == None: id = bpy.data.materials.new("Clay_Render")
				   
	class ExecutePreset(bpy.types.Operator):
		''' Executes a preset '''
		bl_idname = "script.execute"
		bl_label = "Execute a Python Preset"
		
		filepath = bpy.props.StringProperty(name="Path", description="Path of the Python File to execute", maxlen=1024, default="")
		menu_idname = bpy.props.StringProperty(name="Menu ID name", description="ID name of the menu this was called from", default="")
		
		def execute(self, context):
			from os.path import basename
			filepath = self.filepath
			
			# change menu title to the most recently chosen option
			preset_class = getattr(bpy.types, self.menu_idname)
			preset_class.bl_label = bpy.path.display_name(basename(filepath))
			
			# execute the preset using script.python_file_run
			bpy.ops.script.python_file_run(filepath=filepath)
			return {'FINISHED'}
	
	class RenderButtonsPanel():
		bl_space_type = 'PROPERTIES'
		bl_region_type = 'WINDOW'
		bl_context = 'render'
	 
	class RENDER_PT_Clay(RenderButtonsPanel, bpy.types.Panel):
		bl_label = 'Clay Render'  
	 
		def draw_header(self, context):
			layout = self.layout
			layout.label(text="", icon='MATERIAL')
	 
		def draw(self, context):
			layout = self.layout
			sd = context.scene
			rnd = context.scene.render
			rnl = rnd.layers.active
	 
			create_mat()
	 
			split = layout.split()
			col = split.column()
	 
			col.prop(sd, "Clay",)
	 
			col = split.column()
			if bpy.context.scene.Clay!=False:
				id = search()
				col.prop(id, "diffuse_color", text="Clay Color:")
				App_Clay = context.scene.Clay
	
	def register():
		pass
	 
	def unregister():
		rnd = bpy.context.scene.render
		rnl = rnd.layers.active
		rnl.material_override=None
		pass
	 
	if __name__ == "__main__":
		register()
	
############
def Addtheater1():
	
	global  energyfilllamp,energybacklamp,layers,faceminy
	global minx , miny,minz,maxx,maxy,maxz,energymult
	
	# http://www.blender.org/documentation/250PythonDoc/bpy.ops.object.html?highlight=bpy.ops.object.lamp_add#bpy.ops.object.lamp_add
	#defaultworld1()								# Reset to default world settings

	wo = bpy.context.scene.world
	wo.light_settings.use_indirect_light = True 
	bpy.context.scene.world.light_settings.indirect_factor=2.2
	
	print ('  %%%%%%%%%%%%%%%    Executing the Theater function here')
	
	bpy.ops.object.add(type='EMPTY', view_align=False, enter_editmode=False, location=(0.000000, -3.817210, 8.279530), rotation=(0, 0, 0), layers=(layers))
	
	empty1 = bpy.context.object
	empty1.name = 'new_empty'
	
	bpy.ops.object.lamp_add(type='SPOT', view_align=False, location=(19.430519, -20.502472, 7.496113), rotation=(1.614763, 0.709077, 0.853816), layers=(layers))
	lamp1 = bpy.context.object
	
	#Place Empty at the center of the scene
	midx = (minx + maxx)/2
	midy = (miny + maxy)/2
	midz = (minz + maxz)/2
	
	empty1.location.x = midx
	empty1.location.y = midy
	empty1.location.z = midz
	
	### Configure Lighting Setup ###
	lamp1.name = 'volumespot1'						  # Spot Lamp with volume

	lamp1.data.energy = 4.0
	lamp1.data.distance = 25.0
	lamp1.data.spot_size = 1.396264
	lamp1.data.spot_blend = 1
	lamp1.data.shadow_method = 'BUFFER_SHADOW'
	lamp1.data.shadow_buffer_type = 'HALFWAY'
	lamp1.data.shadow_filter_type = 'GAUSS'
	lamp1.data.shadow_buffer_soft = 10
	lamp1.data.shadow_buffer_size = 2048
	lamp1.data.shadow_buffer_bias = 0.100
	lamp1.data.shadow_buffer_samples = 8
	lamp1.data.use_auto_clip_start = True
	lamp1.data.use_auto_clip_end = True
	
	lamp1.location.y = miny
	lamp1.location.x = maxx
	lamp1.location.z = midz	
	
	#Add Track Constraints
	functions.addTrackToConstraint(lamp1,'AutoTrack',empty1)
	
############
def addisocam1():
	
	global  layers
	
	bpy.ops.object.select_pattern(extend=True, pattern="Camera", case_sensitive=False)
	Camdistx=20
	
	rotx=radians(35.26)
	print ('angle x = ',rotx,' rad  = ',degrees(rotx), ' Deg')
	bpy.ops.transform.rotate( value=(rotx,),axis=(1,0,0))
	
	rotz=radians(45)
	print ('angle z = ',rotz,' rad  = ',degrees(rotz), ' Deg')
	bpy.ops.transform.rotate( value=(rotz,),axis=(0,0,1))
	
	# Remove the constraint or calculate the Loc  x y z ?
	a2=90-35.26
	h1=(Camdistx/cos(radians(a2)))
	print ('h1 = ',h1 ,' ang 2 = ',a2,' deg')
	xc1=Camdistx*cos(radians(45))
	yc1=Camdistx*sin(radians(45))
	
	print (' xc1 =',xc1,' yc1 =',yc1)
	return

#############
def  Addstudio1():
	### Add basic 3 point lighting setup ###
	global layers
	global minx, miny, minz, maxx, maxy, maxz, energymult
	
	energy=2
	
	bpy.ops.object.add(type='EMPTY', view_align=False, enter_editmode=False, location=(0.000000, -3.817210, 8.279530), rotation=(0, 0, 0), layers=(layers))
	empty1 = bpy.context.object
	
	object = bpy.context.object
	object.name = 'new_empty'
	
	bpy.ops.object.lamp_add(type='SPOT', view_align=False, location=(19.430519, -20.502472, 7.496113), rotation=(1.614763, 0.709077, 0.853816), layers=(layers))
	lamp1 = bpy.context.object
	
	bpy.ops.object.lamp_add(type='SPOT', view_align=False, location=(-12.848104, 18.574114, 7.496113), rotation=(1.537930, 1.537930, 3.687180), layers=(layers))
	lamp2 = bpy.context.object
	
	bpy.ops.object.lamp_add(type='SPOT', view_align=False, location=(-13.168015, -18.672356, 15.276655), rotation=(0.941318, 0.917498, -1.187617), layers=(layers))
	lamp3 = bpy.context.object
	
	### Configure Lighting Setup ###
	lamp1.name = 'Spot1'
	lamp2.name = 'Spot2'
	lamp3.name = 'Key'

	lamp1.data.energy = 4.0
	lamp1.data.distance = 25.0
	lamp1.data.spot_size = 1.396264
	lamp1.data.spot_blend = 1
	lamp1.data.shadow_method = 'BUFFER_SHADOW'
	lamp1.data.shadow_buffer_type = 'HALFWAY'
	lamp1.data.shadow_filter_type = 'GAUSS'
	lamp1.data.shadow_buffer_soft = 10
	lamp1.data.shadow_buffer_size = 2048
	lamp1.data.shadow_buffer_bias = 0.100
	lamp1.data.shadow_buffer_samples = 8
	lamp1.data.use_auto_clip_start = True
	lamp1.data.use_auto_clip_end = True
	
	lamp2.data.energy = 12.0+energy
	lamp2.data.distance = 25.0
	lamp2.data.spot_size = 1.047198
	lamp2.data.spot_blend = 1
	lamp2.data.shadow_method = 'BUFFER_SHADOW'
	lamp2.data.shadow_buffer_type = 'HALFWAY'
	lamp2.data.shadow_filter_type = 'GAUSS'
	lamp2.data.shadow_buffer_soft = 5
	lamp2.data.shadow_buffer_size = 2048
	lamp2.data.shadow_buffer_bias = 0.100
	lamp2.data.shadow_buffer_samples = 16
	lamp2.data.use_auto_clip_start = True
	lamp2.data.use_auto_clip_end = True
	
	lamp3.data.energy = 12.0+energy
	lamp3.data.distance = 30.0
	lamp3.data.spot_size = 1.570797
	lamp3.data.spot_blend = 1
	lamp3.data.shadow_method = 'BUFFER_SHADOW'
	lamp3.data.shadow_buffer_type = 'HALFWAY'
	lamp3.data.shadow_filter_type = 'GAUSS'
	lamp3.data.shadow_buffer_soft = 20
	lamp3.data.shadow_buffer_size = 2048
	lamp3.data.shadow_buffer_bias = 1
	lamp3.data.shadow_buffer_samples = 16
	lamp3.data.use_auto_clip_start = True
	lamp3.data.use_auto_clip_end = True
	
	functions.addTrackToConstraint(lamp3,'AutoTrack',empty1)
	
	# Add a Wall
	# 2 Faces for  90 degrees corner
	# backwallsize
	# vertsData=[(backwallsize,-backwallsize,-backwallsize),(10,10,-10),(-10,10,-10),(-10,-10,-10),(10,10,10),(-10,10,10)]		# Verts data

	minx = (minx - 3) 
	miny = (miny - 3) 
	minz = (minz - 3) 
	
	maxx = (maxx + 3) 
	maxy = (maxy + 3) 
	maxz = (maxz + 3) 
	
	print()
	print (' minx =',minx,' miny =',miny,' minz =',minz)
	print (' maxx =',maxx,' maxy =',maxy,' maxz =',maxz)
	print()

	vertsData=[(maxx,miny,minz),(maxx,maxy,minz),(minx,maxy,minz),(minx,miny,minz),(maxx,maxy,maxz),(minx,maxy,maxz)]
	# vertsData=[(backwallsize,-backwallsize,-backwallsize),(backwallsize,backwallsize,-backwallsize),(-backwallsize,backwallsize,-backwallsize),(-backwallsize,-backwallsize,-backwallsize),(backwallsize,backwallsize,backwallsize),(-backwallsize,backwallsize,backwallsize)]
	
	facesData=[(0,1,2,3),(1,4,5,2)]																# Faces data
	
	# create new mesh structure
	mesh = bpy.data.meshes.new("myMesh_mesh")				# Create new Mesh 
	mesh.from_pydata(vertsData, [], facesData)				# add data to the mesh
	mesh.update()
	namewall="90degreeswall1"								# change mesh name
	
	new_object = bpy.data.objects.new(namewall, mesh)		# Create new object 
	new_object.data = mesh
	
	scene = bpy.context.scene								# Add object to the scene
	scene.objects.link(new_object)							# link object to the scene
	scene.objects.active = new_object
	new_object.select = True								# select new  object inthe scene
	
	ob=bpy.data.objects[namewall]							# Find object plane 90 degrees wall1
	
	print ('ob=',ob)
	print ('ob=',ob.name)
	
	# http://www.blender.org/documentation/250PythonDoc/bpy.ops.object.html?highlight=bpy.ops.object.modifier#bpy.ops.object.modifier_add
	ob1=bpy.context.object
	print ('bpy.context.object  =',ob1)
	print ()
	
	mod = ob1.modifiers.new(namewall,"SUBSURF")
	mod.levels = 2
																			#   mod.update  ??????????????
	bpy.ops.object.shade_smooth()											# Apply smooth shading
	object=bpy.context.active_object
	myMesh = object.data
	
	ob1.location = [0, 0, 0]
	
	return 
	
#############
#  Spherical Sky dome    See ICeberg file
# http://wiki.blender.org/index.php/Doc:Manual/World/Background
# World Background  as a cube or a sphere
	
def addskydome1():
	
	global  layers
	global minx , miny,minz,maxx,maxy,maxz,energymult
	
	bpy.ops.object.add(type='EMPTY', view_align=False, enter_editmode=False, location=(0,0 ,5), rotation=(0, 0, 0), layers=(layers))
	
	empty1 = bpy.context.object
	empty1.name = 'new_empty'
	
	#Place Empty at the center of the scene
	minx = minx + 1
	miny = miny + 1
	minz = minz + 1
	
	maxx = maxx - 1
	maxy = maxy - 1
	maxz = maxz - 1
	
	midx = (minx + maxx) /2
	midy = (miny + maxy) /2
	midz = (minz + maxz) /2
	
	empty1.location.x = midx
	empty1.location.y = midy+2
	empty1.location.z = midz
	maxscene1=0
	
	print()
	print (' max =',maxx,'  may =',maxy,'  maz =',maxz)
	print()
	
	if abs(maxx)>= abs(maxy) :
		maxscene1=maxx
	else:
		maxscene1=abs(maxy)
	print ('max y  =',maxscene1)
	
	if maxscene1>= abs(maxz) :
		pass
	else:
		maxscene1= abs(maxz)
	
	print()
	print(' Skydome ')
	print (' max =',maxx,'  may =',maxy,'  maz =',maxz)
	
	print()
	
	maxscene1=3.0*maxscene1
	
	# Size of Dome Sphere
	domesize=3.0*maxscene1
	
	print ('Max scene Total =',maxscene1)
	print ('Dome Radius size =',domesize)
	print()

	diamskybox=domesize
	porigin=[0,0,0]
	
	# Hemi lamp
	x0=5.0
	y0=-8.0
	z0=((diamskybox**2.0)-(x0**2.0+y0**2.0))**0.5
	print (' X0=',x0,'Y0=',y0,'z0=',z0,' Rad skydome =',diamskybox)
	print ()
	perc1=0.8
	z0=z0*perc1
	
	print (' X0=',x0,'Y0=',y0,'z0= ',z0,perc1*100.0,' %    Rad skydome =',diamskybox)
	print ()
	
	# Point lamp
	xp0=5.0
	yp0=-8.0
	zp0=((diamskybox**2.0)-(xp0**2.0+yp0**2.0))**0.
	
	percp1=0.8
	zp0=z0*percp1
	
    # This will add a new  primitive UV Sphere
	seg1=32					#  Segments
	ring1=32				#  Rings
    
    #  http://www.blender.org/documentation/250PythonDoc/bpy.ops.mesh.html?highlight=sphere#bpy.ops.mesh.primitive_uv_sphere_add
	
	myuvsphereMesh=bpy.ops.mesh.primitive_uv_sphere_add(segments=seg1,  ring_count=ring1, size=diamskybox, view_align=False, enter_editmode=False, location=(0, 0, 0), rotation=(0, 0, 0), layers=layers)
	obj_act = bpy.context.active_object 
	obj_act.name="Skydome"
	
    #	skydome1=bpy.ops.mesh.primitive_uv_sphere_add(seg1, ring1, size=1, view_align=False, enter_editmode=False, location=(xloc, yloc, zloc), rotation=(rotx, roty, rotz), layer=layers)
	
	bpy.ops.object.shade_smooth()								# Apply smooth shading
	bpy.ops.object.location_apply()								# Apply Location
	
	bpy.context.active_object.draw_type = "WIRE"				# Make dome wiremesh in viewport
	bpy.context.active_object.show_wire = True
	
	namewall="Skydome"
	ob1=bpy.context.object
	mod = ob1.modifiers.new(namewall,"SUBSURF")
	mod.levels = 2
	
	origin=(2,2,2)                    #  ??????????????
	
	red = bpy.data.materials.new('Red')						# Create red material
	red.diffuse_color = (1,0,0)
	red.diffuse_intensity = 0.8
	red.specular_color = (0,1,0)
	red.specular_intensity = 0.2
	red.alpha=0.5
	
	blue = bpy.data.materials.new('Blue')						# Create blue material
	blue.diffuse_color = (0,0,1)
	
	yellow = bpy.data.materials.new('Yellow')					# Create yellow material
	yellow.diffuse_color = (1,1,0)
	
	
	grey1 = bpy.data.materials.new('grey1')					# Create grey1 material
	grey1.diffuse_color = (0.8,0.8,0.8)
	grey1.emit=0.25
	
	
	ob = bpy.context.object										# Add new material to sphere
	me = ob.data
	me.materials.append(grey1)
	
	obmat1 = bpy.context.selected_objects[0] 
	obmat1.active_material = grey1

																# Create procedural texture CLOUDS
	
	text1 = bpy.data.textures.new('CloudTex1', type = 'CLOUDS')
	text1.noise_basis = 'BLENDER_ORIGINAL' 
	text1.noise_scale = 0.25 
	text1.noise_type = 'SOFT_NOISE' 
	text1.saturation = 1 
	
	matext1=grey1.texture_slots.add()							# Create new text slot for given mat  red
	matext1.texture = text1
	matext1.texture_coords = 'ORCO'
	matext1.use_map_color_diffuse = False
	matext1.use_map_color_emission = False 
	matext1.emission_color_factor = 0.5
	matext1.use_map_density = True 
	matext1.mapping = 'FLAT' 
	
    # Assign materials to faces
	
	xhemi=diamskybox*0.5
	yhemi=-diamskybox*0.5
	zhemi=(((diamskybox**2.0)-(x0**2.0+y0**2.0))**0.5)*0.9
	
	xpoint=-diamskybox*0.4
	ypoint=-diamskybox*0.4
	zpoint=(((diamskybox**2.0)-(xp0**2.0+yp0**2.0))**0.5)*0.9
	
	# Distance from  lamp to origin
	
	dpoint=((xpoint)**2.0+(ypoint)**2.0+(zpoint)**2.0)**0.5
	dhemi=((xhemi)**2.0+(yhemi)**2.0+(zhemi)**2.0)**0.5
	
	print(' dist point =',dpoint,' dist hemi =',dhemi)
	
	if bpy.context.scene.Ckeckskydomebright1:
		print (' ^^^^^^^^^^^^^^^^^^^^  got bright ligth here')
	
		bpy.ops.object.lamp_add(type='HEMI', view_align=False, location=(xhemi, yhemi, zhemi), rotation=(0, 0, 0), layers=(layers))
		lamp1 = bpy.context.object
	
		bpy.ops.object.lamp_add(type='POINT', view_align=False, location=(xpoint, ypoint, zpoint), rotation=(0, 0, 0), layers=(layers))
		lamp2 = bpy.context.object
	
	### Configure Lighting Setup ###
		lamp1.name = 'hemi1'
		lamp2.name = 'point1'
		addenergy = 1.0
	
		lamp1.data.energy = 1.0
		lamp1.data.distance = 15.0
		lamp1.data.color=(0.385,0.212,0.212)						# Brownish   Hemi lamp
	
	
		lamp2.data.energy = 1.0
		lamp2.data.distance = 15.0
		lamp2.data.shadow_method = 'RAY_SHADOW'
		lamp2.data.color=(0.509,0.677,0.851)						# Bluish   point lamp
	
	else:
	
		bpy.ops.object.lamp_add(type='HEMI', view_align=False, location=(xhemi, yhemi, zhemi), rotation=(1.537930, 0.711540, 3.687180), layers=(layers))
		lamp1 = bpy.context.object
	
		bpy.ops.object.lamp_add(type='POINT', view_align=False, location=(xpoint, ypoint, zpoint), rotation=(0, 0.0, 0.0), layers=(layers))
		lamp2 = bpy.context.object
	
	### Configure Lighting Setup ###
		lamp1.name = 'hemi1'
		lamp2.name = 'point1'
		addenergy = 1.0
	
		lamp1.data.energy = 1.0
		lamp1.data.distance = 15.0
		lamp1.data.color=(1,1,1)						# white   Hemi lamp
	
	
		lamp2.data.energy = 1.0
		lamp2.data.distance = 15.0
		lamp2.data.shadow_method = 'RAY_SHADOW'
		lamp2.data.color=(1,1,1)						# white   point lamp
	
	#Set Lamp energy
	m =0.05
	lampD = dhemi
	lampE = (lampD * m)
	
	lamp1.data.energy = lampE
	lamp1.data.distance = lampD
	
	print ('lamp 1 ',lamp1.name)
	print (' lampd d=',lampD,' lamp E=',lampE)
	print ()
	
	functions.addTrackToConstraint(lamp1,'AutoTrack',empty1)
	
	#Set Lamp energy
	m =0.15
	lampD1 = dpoint
	lampE1 = (lampD1 * m)
	
	lamp2.data.energy = lampE1
	lamp2.data.distance = lampD1
	
	print()
	print ('lamp 2 ',lamp2.name)
	print (' lampd d1=',lampD1,' lamp E1=',lampE1)
	
############
#	# http://www.blender.org/documentation/250PythonDoc/bpy.ops.object.html?highlight=bpy.ops.object.lamp_add#bpy.ops.object.lamp_add
#	http://en.wikibooks.org/wiki/Blender_3D:_Noob_to_Pro
#	http://en.wikibooks.org/wiki/Blender_3D:_Noob_to_Pro/Faked_Gi_with_Blender_internal
	
def addfakegi():
	global  layers
	global minx, miny, minz, maxx, maxy, maxz, energymult
	
	minx = minx + 1
	miny = miny + 1
	minz = minz + 1
	
	maxx = maxx - 1
	maxy = maxy - 1
	maxz = maxz - 1
	
	midx = (minx + maxx) /2
	midy = (miny + maxy) /2
	midz = (minz + maxz) /2
	
	maxscene1=0
	
	print()
	print (' max =',maxx,'  may =',maxy,'  maz =',maxz)
	print()
	
	if abs(maxx)>= abs(maxy) :
		maxscene1=maxx
	else:
		maxscene1=abs(maxy)
	print ('max y  =',maxscene1)
	
	if maxscene1>= abs(maxz) :
		pass
	else:
		maxscene1= abs(maxz)
	
	print()
	print(' Fake GI')
	print (' max =',maxx,'  may =',maxy,'  maz =',maxz)

	print()
	
	# Back  Wall X 3 scene size = 3 times the scene size  we assume  rectangle wall and floo  here
	
	backwallsize=3.0*maxscene1
	
	# Size of Dome Sphere
	
	domesize=backwallsize/sin(radians(45))
	
	print ('Max scene Total =',maxscene1)
	print ('Backwall size =',backwallsize)
	print ('Dome Radius size =',domesize)
	print()
	
#	diamskybox=bpy.context.scene.skydomeradius
	diamskybox=domesize
	
	print ('Fake GI ')
	
# This will add a new  primitive UV Sphere
	seg1=32					#  Segments
	ring1=32				#  Rings
	
	xloc=2.0				# Sphere location X
	yloc=1.2				# Sphere location Y
	zloc=3.0				# Sphere location Z
	rotx=radians(45)		# Angle given in degrees around global X axis converted to Radians
	roty=radians(0)			# Angle given in degrees around global Y axis converted to Radians
	rotz=radians(0)			# Angle given in degrees around global Z axis converted to Radians
	
#  http://www.blender.org/documentation/250PythonDoc/bpy.ops.mesh.html?highlight=sphere#bpy.ops.mesh.primitive_uv_sphere_add
#myuvsphereMesh=bpy.ops.mesh.primitive_uv_sphere_add(segments=seg1, rings=ring1, size=1, view_align=False, enter_editmode=False, location=(xloc, yloc, zloc), rotation=(rotx, roty, rotz), layer=layers)
	
	myicosphere=bpy.ops.mesh.primitive_ico_sphere_add( subdivisions=2,  size=20.0,  view_align=False,  enter_editmode=False,  location=(0.0,  0.0,  0.0),  rotation=(0.0,  0.0,  0.0),  layers=layers)
	
#	myuvsphereMesh=bpy.ops.mesh.primitive_uv_sphere_add(segments=seg1,  ring_count=ring1, size=diamskybox, view_align=False, enter_editmode=False, location=(0, 0, 0), rotation=(0, 0, 0), layers=layers)
	obj_act = bpy.context.active_object 
	obj_act.name="Skydome"
	
#	skydome1=bpy.ops.mesh.primitive_uv_sphere_add(seg1, ring1, size=1, view_align=False, enter_editmode=False, location=(xloc, yloc, zloc), rotation=(rotx, roty, rotz), layer=layers)
	bpy.context.active_object.draw_type = "WIRE"				# Make dome wiremesh in viewport
	bpy.context.active_object.show_wire = True
	
#	bpy.ops.mesh.flip_normals()								# Flip Normals   ??????????????
	bpy.ops.object.shade_smooth()							# Apply smooth shading
	bpy.ops.object.location_apply()							# Apply Location
	
	origin=(2,2,2)

	bpy.ops.object.select_pattern(extend=True, pattern="Skydome", case_sensitive=False)

	print ('Active object name =  =',obj_act.name )
	myMesh =obj_act.data
	vert_count = obj_act.data.vertices
	qtyv = len(vert_count)
	print (' Vert count =',qtyv)
	
	red = bpy.data.materials.new('Red')						# Create red material
	red.diffuse_color = (1,0,0)
	red.diffuse_intensity = 0.8
	red.specular_color = (0,1,0)
	red.specular_intensity = 0.2
	red.alpha=0.5
	
	blue = bpy.data.materials.new('Blue')					# Create blue material
	blue.diffuse_color = (0,0,1)
	
	yellow = bpy.data.materials.new('Yellow')				# Create yellow material
	yellow.diffuse_color = (1,1,0)
	
	
	grey1 = bpy.data.materials.new('grey1')				# Create grey1 material
	grey1.diffuse_color = (0.8,0.8,0.8)
	grey1.emit=0.25
	
	ob = bpy.context.object									# Add new material to sphere
	me = ob.data
	me.materials.append(grey1)

	# Add a Sun lamp
	bpy.ops.object.lamp_add(type='SUN', view_align=False, location=(0, 0, 0), rotation=(0, 0, 0), layers=(layers))
	lamp1 = bpy.context.object
	
	### Configure Lighting Setup ###
	lamp1.name = 'Sun1'
	
    #Set Lamp energy
	m =0.004
	lampD = domesize /2
	lampE = (lampD * m)
	
	lamp1.data.energy = lampE
	lamp1.data.color=(1.0,0.984,0.575)				# Yellowish sun  light 
	
    #	http://www.blender.org/documentation/250PythonDoc/bpy.ops.object.html?highlight=parent#bpy.ops.object.parent_clear
	bpy.ops.object.select_all(action='DESELECT')
	bpy.ops.object.select_pattern(extend=True, pattern="Sun1", case_sensitive=False)
	
	bpy.ops.object.select_pattern(extend=True, pattern="Skydome", case_sensitive=False)
	bpy.ops.object.parent_set(type ='OBJECT')
	bpy.ops.object.add(type='EMPTY', view_align=False, enter_editmode=False, location=(0.000000, 0, 0), rotation=(0, 0, 0), layers=(layers))

	empty1 = bpy.context.object
	empty1.name = 'empty1'
	
	functions.addTrackToConstraint(lamp1,'AutoTrack',empty1 )
	
	#  ??????????????   lamp don't track to empty 1 in center  
	#  need the rot  value for duplivert ?
	
	bpy.context.scene.objects.active = bpy.context.scene.objects["Skydome"]

#	http://www.blender.org/documentation/250PythonDoc/bpy.types.Object.html?highlight=dupli_type#bpy.types.Object.dupli_type
	ob = bpy.context.active_object
	print ('ob=',ob)
	ob.dupli_type=('FACES')

	#  Rotation  ?
    # Duplivert  and Rot button  ???????????????
	# Add default world  ???????
	# Enable AAO ( Approximate Ambient Occlusion )

	wo = bpy.context.scene.world
	wo.light_settings.use_ambient_occlusion =  True 
	bpy.context.scene.world.light_settings.ao_factor=0.5 
    #	bpy.context.scene.world.light.gather_method = 'APPROXIMATE'  #   ???????????????
    # Add a Wall
    #  2 Faces for  90 degrees corner
    #	backwallsize
    #	vertsData=[(backwallsize,-backwallsize,-backwallsize),(10,10,-10),(-10,10,-10),(-10,-10,-10),(10,10,10),(-10,10,10)]		# Verts data
	
	vertsData=[(backwallsize,-backwallsize,-backwallsize),(backwallsize,backwallsize,-backwallsize),(-backwallsize,backwallsize,-backwallsize),(-backwallsize,-backwallsize,-backwallsize),(backwallsize,backwallsize,backwallsize),(-backwallsize,backwallsize,backwallsize)]
	facesData=[(0,1,2,3),(1,4,5,2)]																# Faces data
	
	
# create new mesh structure
	mesh = bpy.data.meshes.new("myMesh_mesh")				# Create new Mesh 
	mesh.from_pydata(vertsData, [], facesData)				# add data to the mesh
	mesh.update()
	namewall="90degreeswall1"								# change mesh name
	
	new_object = bpy.data.objects.new(namewall, mesh)		# Create new object 
	new_object.data = mesh
	
	scene = bpy.context.scene								# Add object to the scene
	scene.objects.link(new_object)							# link object to the scene
	scene.objects.active = new_object
	new_object.select = True								# select new  object inthe scene
	
	ob=bpy.data.objects[namewall]							# Find object plane 90 degrees wall1
	
	print ('ob=',ob)
	print ('ob=',ob.name)
	
    # http://www.blender.org/documentation/250PythonDoc/bpy.ops.object.html?highlight=bpy.ops.object.modifier#bpy.ops.object.modifier_add
	ob1=bpy.context.object
	print ('bpy.context.object  =',ob1)
	print ()
	
	mod = ob1.modifiers.new(namewall,"SUBSURF")
	mod.levels = 2
	
	bpy.ops.object.shade_smooth()											# Apply smooth shading
	object=bpy.context.active_object
	myMesh = object.data
	print ('Object name =',myMesh.name)
	print ()
	vert_count = bpy.context.active_object.data.vertices
	xv1 = len(vert_count)
	print (' Vert count =',vert_count,' Qty Vert =',xv1 )
	
	# find min Z value to reloacte it 
	print ( ' me.vertices[0].co=',me.vertices[0].co)
	
	minz=0
	
	for ij in range(0, xv1):
		if minz<=me.vertices[ij].co:
			print ('ij=',ij,' Vert loc =',me.vertices[ij].co,' Minz =',minz)
		
	print (' Min z =',minz)

	bpy.context.active_object.location = [0, 0, backwallsize]
	
	return 

##############################################################   Day  set up  ##############
def addBasicsdaylight1():
	global layers,last_menudl1

	#	Set the world for Day light 
	wo = bpy.context.scene.world
	
	wo.use_sky_paper=True
	wo.use_sky_blend=True
	wo.use_sky_real=True
	
	wo.light_settings.use_ambient_occlusion = True
	
	bpy.context.scene.world.horizon_color[0]=0.05
	bpy.context.scene.world.horizon_color[1]=0.05
	bpy.context.scene.world.horizon_color[2]=0.05
	
	bpy.context.scene.world.zenith_color[0]=0.41			# Bluish  sky Zenith
	bpy.context.scene.world.zenith_color[1]=0.447
	bpy.context.scene.world.zenith_color[2]=0.862
	
	bpy.context.scene.world.ambient_color[0]=0.0
	bpy.context.scene.world.ambient_color[1]=0.0
	bpy.context.scene.world.ambient_color[2]=0.0
	
	### Add basic Daylight lighting setup ###
	bpy.ops.object.add(type='EMPTY', view_align=False, enter_editmode=False, location=(0.000000, 10.0, 10.0), rotation=(0, 0, 0), layers=(layers))
	empty1 = bpy.context.object
	
	object = bpy.context.object
	object.name = 'new_empty'
	
	bpy.ops.object.lamp_add(type='SUN', view_align=False, location=(10, 3, 15), rotation=(1.614763, 0.709077, 0.853816), layers=(layers))
	lamp1 = bpy.context.object
	
	# http://www.blender.org/documentation/250PythonDoc/bpy.ops.object.html?highlight=bpy.ops.object.lamp_add#bpy.ops.object.lamp_add
	bpy.ops.object.lamp_add(type='HEMI', view_align=False, location=(12, 4, 18), rotation=(1.537930, 0.711540, 3.687180), layers=(layers))
	lamp2 = bpy.context.object

	### Configure Lighting Setup ###
	lamp1.name = 'Sun1'
	addenergy = bpy.context.scene.energy
	
	lamp1.data.energy = 1.0+addenergy
	lamp1.data.distance = 25.0
	lamp1.data.color=(1.0,0.984,0.575)				# Yellowish sun  light 
	
	lamp2.data.energy = 0.57+addenergy
	lamp2.data.distance = 15.0
	lamp2.data.color=(0.2,0.22,1.0)					# Bluish light for shadow
	
	# select and scale the domain :D
	bpy.ops.object.select_pattern(extend=False, pattern="Domain", case_sensitive=False)
	if "Domain" in bpy.data.objects:
		bpy.context.active_object.scale = (150,150,150)
	
	return 

############
def adddaycloud22():

	global layers,last_menudl1

	#	Set the world for Day cloudy light 
	wo = bpy.context.scene.world

	wo.use_sky_paper=True
	wo.use_sky_blend=True
	wo.use_sky_real=True
	
	wo.light_settings.use_ambient_occlusion = True
	wo.light_settings.ao_factor =0.42
	
	bpy.context.scene.world.horizon_color[0]=0.05
	bpy.context.scene.world.horizon_color[1]=0.05
	bpy.context.scene.world.horizon_color[2]=0.05
	
	bpy.context.scene.world.zenith_color[0]=0.23			# Dark blue sky Zenith
	bpy.context.scene.world.zenith_color[1]=0.28
	bpy.context.scene.world.zenith_color[2]=0.6
	
	bpy.context.scene.world.ambient_color[0]=0.0
	bpy.context.scene.world.ambient_color[1]=0.0
	bpy.context.scene.world.ambient_color[2]=0.0
	
	### Add basic Daylight lighting setup ###
	bpy.ops.object.add(type='EMPTY', view_align=False, enter_editmode=False, location=(0.000000, 10.0, 10.0), rotation=(0, 0, 0), layers=(layers))
	empty1 = bpy.context.object
	
	object = bpy.context.object
	object.name = 'new_empty'
	
	bpy.ops.object.lamp_add(type='SUN', view_align=False, location=(10, 3, 15), rotation=(1.614763, 0.709077, 0.853816), layers=(layers))
	lamp1 = bpy.context.object
	
	# http://www.blender.org/documentation/250PythonDoc/bpy.ops.object.html?highlight=bpy.ops.object.lamp_add#bpy.ops.object.lamp_add
	bpy.ops.object.lamp_add(type='HEMI', view_align=False, location=(12, 4, 18), rotation=(1.537930, 0.711540, 3.687180), layers=(layers))
	lamp2 = bpy.context.object
	
	### Configure Lighting Setup ###
	lamp1.name = 'Sun1'
	addenergy = bpy.context.scene.energy
	
	lamp1.data.energy = 0.5+addenergy
	lamp1.data.distance = 25.0
	lamp1.data.color=(1.0,0.984,0.575)				# Yellowish sun light 
	
	
	lamp2.data.energy = 0.5+addenergy
	lamp2.data.distance = 15.0
	lamp2.data.color=(0.2,0.22,1.0)					# Bluish light for shadow
	
	# select and scale the domain :D
	bpy.ops.object.select_pattern(extend=False, pattern="Domain", case_sensitive=False)
	
	if "Domain" in bpy.data.objects:
		bpy.context.active_object.scale = (150,150,150)

############
def func101():
	global layers,last_menudl1
	
	# Set the  World  for  Day light  Setup 
	# http://www.blender.org/documentation/250PythonDoc/bpy.ops.object.html?highlight=bpy.ops.object.lamp_add#bpy.ops.object.lamp_add
	#	Set the world for Day cloudy light 
	
	wo = bpy.context.scene.world
	
	wo.use_sky_paper=True
	wo.use_sky_blend=True
	wo.use_sky_real=True
	
	wo.light_settings.use_ambient_occlusion = True
	wo.light_settings.ao_factor =0.42
	
	bpy.context.scene.world.horizon_color[0]=0.05
	bpy.context.scene.world.horizon_color[1]=0.05
	bpy.context.scene.world.horizon_color[2]=0.05
	
	bpy.context.scene.world.zenith_color[0]=0.5			# Greyish sky Zenith
	bpy.context.scene.world.zenith_color[1]=0.5
	bpy.context.scene.world.zenith_color[2]=0.5
	
	bpy.context.scene.world.ambient_color[0]=0.0
	bpy.context.scene.world.ambient_color[1]=0.0
	bpy.context.scene.world.ambient_color[2]=0.0
	
	### Add basic Daylight lighting setup ###
	bpy.ops.object.add(type='EMPTY', view_align=False, enter_editmode=False, location=(0.000000, 10.0, 10.0), rotation=(0, 0, 0), layers=(layers))
	empty1 = bpy.context.object
	
	object = bpy.context.object
	object.name = 'new_empty'
	
	bpy.ops.object.lamp_add(type='SUN', view_align=False, location=(10, 3, 15), rotation=(1.614763, 0.709077, 0.853816), layers=(layers))
	lamp1 = bpy.context.object
	
	# http://www.blender.org/documentation/250PythonDoc/bpy.ops.object.html?highlight=bpy.ops.object.lamp_add#bpy.ops.object.lamp_add
	bpy.ops.object.lamp_add(type='HEMI', view_align=False, location=(12, 4, 18), rotation=(1.537930, 0.711540, 3.687180), layers=(layers))
	lamp2 = bpy.context.object
	
	### Configure Lighting Setup ###
	lamp1.name = 'Sun1'
	addenergy = bpy.context.scene.energy
	
	lamp1.data.energy = 0.5+addenergy
	lamp1.data.distance = 25.0
	lamp1.data.color=(1.0,0.984,0.575)				# Yellowish sun  light 
	
	
	lamp2.data.energy = 0.5+addenergy
	lamp2.data.distance = 15.0
	lamp2.data.color=(0.2,0.22,1.0)					# Bluish light for shadow
	
	# select and scale the domain :D
	bpy.ops.object.select_pattern(extend=False, pattern="Domain", case_sensitive=False)
	if "Domain" in bpy.data.objects:
		bpy.context.active_object.scale = (150,150,150)

############
#def Adddaysunset32():
def func103():
	global layers,last_menudl1
	
	# http://www.blender.org/documentation/250PythonDoc/bpy.ops.object.html?highlight=bpy.ops.object.lamp_add#bpy.ops.object.lamp_add
	wo = bpy.context.scene.world
	wo.use_sky_paper=True
	wo.use_sky_blend=True
	wo.use_sky_real=True
	
	wo.light_settings.use_ambient_occlusion = True
	wo.light_settings.ao_factor =0.42

	#	Set the world for Day sunset  light 
	bpy.context.scene.world.horizon_color[0]=0.5
	bpy.context.scene.world.horizon_color[1]=0.5
	bpy.context.scene.world.horizon_color[2]=0.5
	
	bpy.context.scene.world.zenith_color[0]=0.711				# Redish sun  light 
	bpy.context.scene.world.zenith_color[1]=0.161
	bpy.context.scene.world.zenith_color[2]=0.179
	
	bpy.context.scene.world.ambient_color[0]=0.5
	bpy.context.scene.world.ambient_color[1]=0.5
	bpy.context.scene.world.ambient_color[2]=0.5

	### Add basic Daylight lighting setup ###
	bpy.ops.object.add(type='EMPTY', view_align=False, enter_editmode=False, location=(0.000000, 0.0, 0.0), rotation=(0, 0, 0), layers=(layers))
	empty1 = bpy.context.object
	
	object = bpy.context.object
	object.name = 'new_empty'
	
	bpy.ops.object.lamp_add(type='SUN', view_align=False, location=(19.430519, 10, 10), rotation=(0, 0, 0), layers=(layers))
	lamp1 = bpy.context.object
	
	### Configure Lighting Setup ###
	lamp1.name = 'Sun1'
	
	lamp1.data.energy = 4.0
	lamp1.data.distance = 25.0
	lamp1.data.color=(0.1,0.1,0.7)				# Bluish sun  light 
	
	# select and scale the domain :D
	bpy.ops.object.select_pattern(extend=False, pattern="Domain", case_sensitive=False)
	if "Domain" in bpy.data.objects:
		bpy.context.active_object.scale = (150,150,150)

############
#def Adddaysunrise32():
def func102():

	global layers,last_menudl1
	
	# http://www.blender.org/documentation/250PythonDoc/bpy.ops.object.html?highlight=bpy.ops.object.lamp_add#bpy.ops.object.lamp_add
	wo = bpy.context.scene.world
	
	wo.use_sky_paper=True
	wo.use_sky_blend=True
	wo.use_sky_real=True
	
	wo.light_settings.use_ambient_occlusion = True
	wo.light_settings.ao_factor =0.42
	
	
	#	Set the world for Day light 
	bpy.context.scene.world.horizon_color[0]=0.5
	bpy.context.scene.world.horizon_color[1]=0.5
	bpy.context.scene.world.horizon_color[2]=0.5
	
	bpy.context.scene.world.zenith_color[0]=0.5
	bpy.context.scene.world.zenith_color[1]=0.5
	bpy.context.scene.world.zenith_color[2]=0.5
	
	bpy.context.scene.world.ambient_color[0]=0.5
	bpy.context.scene.world.ambient_color[1]=0.5
	bpy.context.scene.world.ambient_color[2]=0.5
	
	### Add basic Daylight lighting setup ###
	bpy.ops.object.add(type='EMPTY', view_align=False, enter_editmode=False, location=(0.000000, 0.0, 0.0), rotation=(0, 0, 0), layers=(layers))
	empty1 = bpy.context.object
	
	object = bpy.context.object
	object.name = 'new_empty'
	
	bpy.ops.object.lamp_add(type='SUN', view_align=False, location=(19.430519, 10, 10), rotation=(0, 0, 0), layers=(layers))
	lamp1 = bpy.context.object
	
	
	### Configure Lighting Setup ###
	lamp1.name = 'Sun1'
	addenergy = bpy.context.scene.energy
	
	
	lamp1.data.energy = 1.0+addenergy
	lamp1.data.distance = 25.0
	lamp1.data.color=(0.9,0.1,0.1)		
	
	# select and scale the domain :D
	bpy.ops.object.select_pattern(extend=False, pattern="Domain", case_sensitive=False)
	if "Domain" in bpy.data.objects:
		bpy.context.active_object.scale = (150,150,150)
	
	
############
def Adddayclearnight42():
	
	global layers,last_menudl1
	
	# http://www.blender.org/documentation/250PythonDoc/bpy.ops.object.html?highlight=bpy.ops.object.lamp_add#bpy.ops.object.lamp_add
	defaultworld1()											# Reset to default world settings
	
	#	Set the world for clear night light 
	bpy.context.scene.world.horizon_color[0]=0.0
	bpy.context.scene.world.horizon_color[1]=0.0
	bpy.context.scene.world.horizon_color[2]=0.0
	
	bpy.context.scene.world.zenith_color[0]=0.1				# Dark blue  sky  Zenith
	bpy.context.scene.world.zenith_color[1]=0.1
	bpy.context.scene.world.zenith_color[2]=0.9
	
	bpy.context.scene.world.ambient_color[0]=0.0
	bpy.context.scene.world.ambient_color[1]=0.0
	bpy.context.scene.world.ambient_color[2]=0.0
	
	wo = bpy.context.scene.world
	bpy.context.scene.world.light_settings.use_environment_light =True
	bpy.context.scene.world.light_settings.environment_energy=0.4
	
	### Add basic clear night  lighting setup ###
	bpy.ops.object.add(type='EMPTY', view_align=False, enter_editmode=False, location=(0.000000, 0.0, 0.0), rotation=(0, 0, 0), layers=(layers))
	empty1 = bpy.context.object
	
	object = bpy.context.object
	object.name = 'new_empty'
	
	bpy.ops.object.lamp_add(type='SUN', view_align=False, location=(19.430519, 10, 10), rotation=(0, 0, 0), layers=(layers))
	lamp1 = bpy.context.object

	### Configure Lighting Setup ###
	lamp1.name = 'Sun1'
	
	lamp1.data.energy = 1.0
	lamp1.data.distance = 25.0
	lamp1.data.color=(0.2,0.1,0.95)							# Bluish dark sun  light 
	
	# select and scale the domain :D
	bpy.ops.object.select_pattern(extend=False, pattern="Domain", case_sensitive=False)
	if "Domain" in bpy.data.objects:
		bpy.context.active_object.scale = (150,150,150)

###########
def Adddaycloudynight52():
	
	global layers,last_menudl1
	
	# http://www.blender.org/documentation/250PythonDoc/bpy.ops.object.html?highlight=bpy.ops.object.lamp_add#bpy.ops.object.lamp_add
	defaultworld1()										# Reset to default world settings
	
	#	Set the world for clear night light 
	bpy.context.scene.world.horizon_color[0]=0.0
	bpy.context.scene.world.horizon_color[1]=0.0
	bpy.context.scene.world.horizon_color[2]=0.0
	
	bpy.context.scene.world.zenith_color[0]=0.1			# Dark blue  sky  Zenith
	bpy.context.scene.world.zenith_color[1]=0.1
	bpy.context.scene.world.zenith_color[2]=0.9
	
	bpy.context.scene.world.ambient_color[0]=0.0
	bpy.context.scene.world.ambient_color[1]=0.0
	bpy.context.scene.world.ambient_color[2]=0.0
	
	wo = bpy.context.scene.world
	bpy.context.scene.world.light_settings.use_environment_light =True
	bpy.context.scene.world.light_settings.environment_energy=0.1
	
	### Add basic Daylight lighting setup ###
	bpy.ops.object.add(type='EMPTY', view_align=False, enter_editmode=False, location=(0.000000, 0.0, 0.0), rotation=(0, 0, 0), layers=(layers))
	empty1 = bpy.context.object
	
	object = bpy.context.object
	object.name = 'new_empty'
	
	bpy.ops.object.lamp_add(type='SUN', view_align=False, location=(19.430519, 10, 10), rotation=(0, 0, 0), layers=(layers))
	lamp1 = bpy.context.object
	
	### Configure Lighting Setup ###
	lamp1.name = 'Sun1'
	
	lamp1.data.energy = 4.0					#  ??????????????????????
	lamp1.data.distance = 25.0
	
	# select and scale the domain :D
	bpy.ops.object.select_pattern(extend=False, pattern="Domain", case_sensitive=False)
	if "Domain" in bpy.data.objects:
		bpy.context.active_object.scale = (150,150,150)
	

#################
#	To delete texture map
#	bpy.context.scene.world.texture_slots.clear(0)
	
def world_Angularmap1():
	
	print ('begining of Angular map1 ')
	
	defaultworld1()
	
	world = bpy.context.scene.world
	world.name = 'Angular_mapping'
	world.horizon_color = (0,0,0)
	world.zenith_color = (0,0,0)
	world.ambient_color = (0,0,0)
	
	world.use_sky_real =True
	world.use_sky_paper = False
	world.use_sky_blend=False
	
	
	world.light_settings.use_ambient_occlusion = False 
	world.light_settings.use_environment_light =True
	world.light_settings.use_indirect_light = False
	
	bpy.context.scene.world.light_settings.environment_energy=1.0
	
	world.mist_settings.use_mist = False
	world.star_settings.use_stars = False
	world.light_settings.environment_color="SKY_TEXTURE"
	bpy.context.scene.world.light_settings.gather_method == 'APPROXIMATE'
	
    # angular map texture added to world
	tex = bpy.data.textures.new('texture', type = 'IMAGE')
	textimage1 = bpy.data.worlds[0].texture_slots.add()
	textimage1.texture = tex
	textimage1.texture_coords = 'ANGMAP'
	textimage1.use_map_horizon = 1
	textimage1.use_map_blend = 0
	
################
def world_skymap1():
	
	defaultworld1()
	
	print ('begining of skymap1 ')
	
	world = bpy.context.scene.world
	world.name = 'Sky_mapping'
	world.horizon_color = (0.051,0.051,0.051)
	world.zenith_color = (0.01,0.01,0.01)
	world.ambient_color = (0,0,0)
	
	world.use_sky_real =True
	world.use_sky_paper = False
	world.use_sky_blend=False
	
	
	world.light_settings.use_ambient_occlusion = True
	world.light_settings.use_environment_light =True
	world.light_settings.use_indirect_light = False
	
	bpy.context.scene.world.light_settings.ao_factor=0.02 
	
	bpy.context.scene.world.light_settings.environment_energy=1.0
	
	world.mist_settings.use_mist = False
	world.star_settings.use_stars = False
	world.light_settings.environment_color="SKY_TEXTURE"
	bpy.context.scene.world.light_settings.gather_method == 'APPROXIMATE'
	
	tex = bpy.data.textures.new('texture', type = 'IMAGE')
	
	textimage1 = bpy.data.worlds[0].texture_slots.add()
	textimage1.texture = tex
	textimage1.texture_coords = 'SPHERE'
	textimage1.use_map_horizon = 1
	textimage1.use_map_blend = 0

#	http://wiki.blender.org/index.php/Doc:Manual/World/Background	
#### World  Angular mapping  ####
	
def world_HDRI1():
	
	print ('begining of world_HDRI1 ')
	
	defaultworld1()
	
	world = bpy.context.scene.world
	world.name = 'HDRI_mapping'
	world.horizon_color = (0,0,0)
	world.zenith_color = (0,0,0)
	world.ambient_color = (0,0,0)
	
	world.use_sky_real =True
	world.use_sky_paper = False
	world.use_sky_blend=False
	
	
	world.light_settings.use_ambient_occlusion = False 
	world.light_settings.use_environment_light =True
	world.light_settings.use_indirect_light = False
	
	bpy.context.scene.world.light_settings.environment_energy=1.0
	
	world.mist_settings.use_mist = False
	world.star_settings.use_stars = False
	world.light_settings.environment_color="SKY_TEXTURE"
	bpy.context.scene.world.light_settings.gather_method == 'APPROXIMATE'
	tex = bpy.data.textures.new('texture', type = 'IMAGE')
	textimage1 = bpy.data.worlds[0].texture_slots.add()
	textimage1.texture = tex
	textimage1.texture_coords = 'ANGMAP'
	textimage1.use_map_horizon = 1
	textimage1.use_map_blend = 0
	print ('Hello  HDRI   function here ')
	
###############
# ONE POINT
############
	
def register():

	#### SCENE TYPE MENU ####			# Menu Level 1
	bpy.types.Scene.menu_options = bpy.props.EnumProperty(name='Scene Type', items=[
		('1','Lamps lighting set up','1'),
		('2','Exterior lighting set up','2'),
		('3','World Light set up','3'),
		('4','AO','4'),
		('5','Sky Dome  / GI lighting set up','5'),
		('6','Fluo fixture set up','6'),
		('7','General render','7'),
		('8','Special Light set up','8'),
		('9','Other light set up','9'),
		('10','Ang / Sky / HDRI mapt set up','10')
		])

    ################   Lamps  second Level menu
	#### Lamp Lighting set up #### 					# Menu Level 2 
	bpy.types.Scene.my_menu_choice = bpy.props.EnumProperty(name='Lamps set up lighting', items=[
		('1','One Lamp Lighting set up','1'),
		('2','Two Lamps Lighting set up','2'),
		('3','Three Lamps Lighting set up','3'),
		('4','Four Lamps Lighting set up','4')
		])
	
	################   Lamps  Third Level menu
	#### Lamp ONE Light set up ####								# Menu Level 3 
	bpy.types.Scene.menu_one_point = bpy.props.EnumProperty(name=' ONE Light set upPreset', items=[
		('1','One Point Light set up','1'),
		('2','One Spot light set up','2'),
		('3','One Area light set up','3'),
		('4','One Hemi light set up','4'),
		('5','One Volumetric Spot light set up','5'),
		])
	
	#### Lamps TWO Light set up  #### 							# Menu Level 3 
	bpy.types.Scene.menu_two_point = bpy.props.EnumProperty(name='TWO Light set up Preset', items=[
		('1','Two Point Lighting High Contrast 1','1'),
		('2','Two Point Lighting High Contrast 2 ','2'),
		('3','Two Point Behind Lighting ','3'),
		('4','Two Point Dramatic Lighting ','4'),
		])
	
	#### Lamps THREE Light set up ####							# Menu Level 3
	bpy.types.Scene.menu_three_point = bpy.props.EnumProperty(name='THREE Light set up Preset', items=[
		('1','Three Spot Light ','1'),
		('2','Three Area Light','2')
		])
	
	#### Lamps FOUR Light set up #### 							# Menu Level 3
	bpy.types.Scene.menu_four_point = bpy.props.EnumProperty(name='FOUR Light set up Preset', items=[
		('1','Four Spot Lighting','1'),
		('2','Effect Lighting','2')
		])

	#### OUTDOOR / Exterior  OPTIONS ####				# Menu Level 2
	bpy.types.Scene.menu_outdoor = bpy.props.EnumProperty(name='Exterior set up', items=[
		('1','Day light set up','1'),
		('2','Cloudy day','2'),
		('3','Overcast day','3'),
		('4','Sun rise','4'),
		('5','Sun set','5'),
		('6','Clear night','6'),
		('7','Overcast cloudy night','7'),
		('8','Quarter Moon Lighting','8'),
		('9','Half Moon Lighting','9'),
		('10','Three-Quarter Moon Lighting','10'),
		('11','Full Moon Lighting','11'),
		('12','Night No Moon','12')
		])
	
	#### World light set up ####						# Menu Level 2
	bpy.types.Scene.menu_world = bpy.props.EnumProperty(name='World light set up', items=[
		('1','Environment','1'),
		('2','Indirect','2'),
		('3','Indirect/Environment mixed light set up','3')
		])
	
	#### AO set up ####						# Menu Level 2
	bpy.types.Scene.menu_AO = bpy.props.EnumProperty(name='AO set up', items=[
		('1','AO Light set up','1'),
		('2','AO  indirect set up','2'),
		('3','FAke AO  16 LAmps','3'),
		('4','AAO Light set up','4')
		])
	
	#### Sky Dome set up ####						# Menu Level 2
	bpy.types.Scene.skydome_menu = bpy.props.EnumProperty(name='Sky Dome', items=[
		('1','SKy Dome 1','1'),
		('2','Fake GI Indir','2')
		])
	
	#### Fluorescent set up ####					# Menu Level 2
	bpy.types.Scene.menu_Fluo = bpy.props.EnumProperty(name='Fluorescent set up', items=[
		('1','2 X 4 Fluo Transp refractor','1'),
		('2','1 X 4 Fluo / Fin set up','2'),
		('3','Fluo Strips','3'),
		('4','Fluo Strips Deco','4'),
		('5','Fluo Watertight','5'),
		('6','Fluo Industriel','6'),
		('7','Fluo Other','7')
		])
	
	#### General menu set up ####					# Menu Level 2
	bpy.types.Scene.menu_gen = bpy.props.EnumProperty(name='General set up', items=[
		('1','Clay  Render','1'),
		('2','Sepia Photo Render','2'),
		('3','Sepia Scene Render','3'),
		('4','Sketchup style Render','4')
		])
	
	#### Light special  set up  ####						# Menu Level 2
	bpy.types.Scene.menu_special = bpy.props.EnumProperty(name='Special Light set up', items=[
		('1','Area Light Set up','1'),
		('2','Studio Light Set up','2'),
		('3','Light Box 3','3'),
		('4','Light Box 4','4'),
		('5','Theather light / smoke','5'),
		('6','Theather 3 color light / smoke','6')
		])
	
	#### Other menu set up ####								# Menu Level 2
	bpy.types.Scene.menu_other = bpy.props.EnumProperty(name='Other set up', items=[
		('1','Camera Isometric Set up','1'),
		('2','Camera Dimetric Set up','2'),
		('3','Camera Trimetric Set up','3')
		])
	
	#### Ang SKy HDRI map  menu set up ####								# Menu Level 2
	bpy.types.Scene.menu_angmap1 = bpy.props.EnumProperty(name='Ang / Sky HDRI mapping set up', items=[
		('1','Angular Map Set up','1'),
		('2','Sky Map Set up','2'),
		('3','HDRI Set up','3')
		])
	
	#### CHECKBOX PROPERTYS ####
	bpy.types.Scene.use_addon_objects = bpy.props.BoolProperty(
		name='Use Add-On Objects',
		default=False,
		description='only check this if Wizard Objects Add_On is enabled')
		
	#### STRING PROPERTYS ####
	bpy.types.Scene.type_of_lighting_added = bpy.props.StringProperty(
		name='Current Selection')
	
	bpy.utils.register_class(lightingpanel)
	bpy.utils.register_class(addOperator)
	bpy.utils.register_class(removeOperator)
	
##################	
def unregister():
	
	bpy.utils.unregister_class(lightingpanel)
	bpy.utils.unregister_class(addOperator)
	bpy.utils.unregister_class(removeOperator)

if __name__ == "__main__":
	register()