# -*- coding: utf-8 -*-
"""
Created on Tue Feb  2 11:25:48 2016

@author: gray

This is a lightsource algorithm for benny's roguelike game, using RPAS
as per https://github.com/MoyTW/roguebasin_rpas/blob/master/rpas.py

Facing: 0123 -> LRDU -> WESN
"""

#NOTE: You only need to import LightSource from this file

import numpy as np
import pdb

class CellAngles(object):
    '''Used by the RPAS algorithm to calculate the angles between grid cells'''
    def __init__(self, near, center, far):
        self.near = near
        self.center = center
        self.far = far

    def __repr__(self):
        return "(near={0} center={1} far={2})".format(self.near, self.center, self.far)


class GeoMask(object):
    '''The default mask is just a completely open area.'''
    def __init__(self, origin=(0,0), radius=1):
        self.radius = radius
        self.ox, self.oy = origin
        self.points = set()
        
    
    @property
    def _mask(self):
        return np.full((self.radius, self.radius), True)
    
    def change_radius(self, newradius):
        self.radius = newradius
        self._update_points()
    
    def change_origin(self, origin):
        self.ox, self.oy = origin
        self._update_points()

    def _update_points(self):
        xi, yi = self._mask.nonzero()
        xi.flags.writeable = yi.flags.writeable = True
        xi = xi-self.radius+self.ox
        yi = yi-self.radius+self.oy
        self.points = set(zip(xi, yi))
        


class Cone(GeoMask):
    '''A circular sector mask'''
    name = "cone"
    FACING_ANGLE = [180., 0., 90., 270.]
    
    def __init__(self, facing=0, angle=90., **kw):
        super(Cone, self).__init__(**kw)
        self.facing = facing
        self.angle = angle
        self._update_points()
    
    def __setstate__(self,state):
        self.radius = state["radius"]
        self.ox,self.oy = state["origin"]
        self.facing = state["facing"]
        self.angle = state["angle"]
        self._update_points()
        
    def __getstate__(self):
        return {"radius":self.radius,"origin":(self.ox,self.oy),"facing":self.facing,"angle":self.angle}    
    
    @property
    def angle_range(self):
        fa = self.FACING_ANGLE[self.facing]
        ha = self.angle/2.
        return np.radians([fa-ha, fa+ha])
    
    @property
    def _mask(self):
        x, y = np.mgrid[-self.radius:self.radius+1, -self.radius:self.radius+1]
        tmin, tmax = self.angle_range
        
        r2 = x*x + y*y
        theta = np.arctan2(x,y) - tmin
        theta %= (2.*np.pi)
        circmask = r2 <= (self.radius * self.radius)
        conemask = theta <= (tmax - tmin)
        conemask[self.radius,self.radius] = True
        return conemask
        return circmask * conemask
    
    def change_facing(self, newfacing):
        self.facing = newfacing
        self._update_points

class Circle(GeoMask):
    '''A circular mask'''
    name = "circle"
    def __init__(self, **kw):
        super(Circle, self).__init__(**kw)
        self._update_points()
        
    def __setstate__(self,state):
        self.radius = state["radius"]
        self.ox,self.oy = state["origin"]
        self._update_points()
        
    def __getstate__(self):
        return {"radius":self.radius,"origin":(self.ox,self.oy)}
        
    @property
    def _mask(self):
        x, y = np.mgrid[-self.radius:self.radius+1, -self.radius:self.radius+1]
        return (x*x+y*y) <= (self.radius*self.radius)

class default_decay(object):
    '''The default decay algorithm is just simply reducing the radius by 1 
    every time step.'''
    def __init__(self, radius):
        self.duration = 0
        self.radius = radius
        self.done = False
    
    def __call__(self):
        if self.duration == self.radius: 
            self.done = True
            return 0
        self.duration += 1
        return self.radius - self.duration


class LightSource(object):
    '''This is the actual class which calculates the grid cells included in
    the lit area. The "walls" argument is just a boolean array which is True
    at wall tiles and False at floor tiles; should be straightforward to construct
    from the gmap.
    
    This lightsource class can handle decaying radii with the update_decay function.
    Passing decay='default' uses the default decay algorithm above; other algorithms
    can easily be added. Whenever the decay has completely killed the light strength,
    decay.done = True which sets self.on = False, and the instance can be garbage-
    collected.
    
    Only update_decay, change_orientation, change_position, and the lit property
    should be accessed from outside.
    '''
    RADIUS_FUDGE = 1.0 / 3.0
    NOT_VISIBLE_BLOCKS_VISION = True
    RESTRICTIVENESS = 1
    VISIBLE_ON_EQUAL = True
    
    def __init__(self, walls, origin=(0,0), radius=3, decay=None, 
                 shape='circle', oriented=False, **kw):
        self._shape = {'cone':Cone,'circle':Circle}[shape](origin=origin, radius=radius, **kw)
        self.radius = radius
        self.x, self.y = origin
        self.on = True
        if decay == 'default':
            self.decay = default_decay(self.radius)
        else:
            self.decay = decay
        self.oriented = oriented
        self._walls = ~walls
        self.visible = set()
        self._update_visible()
        #pdb.set_trace()
    
    def __setstate__(self,state):
        self._shape = {'cone':Cone,'circle':Circle}[state["shape"]]
        self._shape.__setstate__(state["shapestate"])
        self.radius = state["radius"]
        self.on,self.x,self.y = state["on"],state["x"],state["y"]
        self.oriented = state["oriented"]
        self._walls = np.array(state["walls"])
        self._update_visible()
    def __getstate__(self):
        return {"shape":self._shape.name, "shapestate":self._shape.__getstate__(),"radius":self.radius,
                "on":self.on,"x":self.x,"y":self.y,"oriented":self.oriented,"walls":self._walls.tolist()}
    
    def _transparent(self, x, y):
        return self._walls[x,y]
    
    def update_decay(self, callback=None):
        if self.decay is None:
            return
        self._shape.update_radius(self.decay())
        self._update_visible()
        if self.decay.done:
            self.on = False
    
    def change_orientation(self, new_orientation):
        if not self.oriented:
            return
        self._shape.change_facing(new_orientation)
    
    def change_position(self, new_x, new_y):
        self.x, self.y = new_x, new_y
        self._shape.change_origin((new_x, new_y))
        self._update_visible()
    
    @property
    def lit(self):
        return self._shape.points & self._visible
    
    ###From here on down is the Restrictive Precise Angle Shadowcasting algorithm
    
    def _update_visible(self):
        self._visible = self._visible_cells_in_quadrant_from(1, 1)
        self._visible.update(self._visible_cells_in_quadrant_from(1, -1))
        self._visible.update(self._visible_cells_in_quadrant_from(-1, -1))
        self._visible.update(self._visible_cells_in_quadrant_from(-1, 1))
        self._visible.add((self.x, self.y))
    
    def _visible_cells_in_quadrant_from(self, quad_x, quad_y):
        cells = self._visible_cells_in_octant_from(quad_x, quad_y, True)
        cells.update(self._visible_cells_in_octant_from(quad_x, quad_y,
                                                        False))
        return cells
    
    def _visible_cells_in_octant_from(self, quad_x, quad_y, is_vertical):
        iteration = 1
        visible_cells = set()
        obstructions = list()

        while iteration <= self.radius and not (len(obstructions) == 1 and
                                                obstructions[0].near == 0.0 and 
                                                obstructions[0].far == 1.0):
            num_cells_in_row = iteration + 1
            angle_allocation = 1.0 / float(num_cells_in_row)

            # Start at the center (vertical or horizontal line) and step outwards
            for step in range(iteration + 1):
                cell = self._cell_at(quad_x, quad_y, step, iteration, is_vertical)

                if self._cell_in_radius(cell):
                    cell_angles = CellAngles(near=(float(step) * angle_allocation),
                                             center=(float(step + .5) * angle_allocation),
                                             far=(float(step + 1) * angle_allocation))

                    if self._cell_is_visible(cell_angles, obstructions):
                        visible_cells.add(cell)
                        if not self._transparent(*cell):
                            obstructions = self._add_obstruction(obstructions, cell_angles)
                    elif self.NOT_VISIBLE_BLOCKS_VISION:
                        obstructions = self._add_obstruction(obstructions, cell_angles)
            iteration += 1
        return visible_cells
    
    def _cell_at(self, quad_x, quad_y, step, iteration, is_vertical):
        if is_vertical:
            cell = (self.x + step * quad_x, self.y + iteration * quad_y)
        else:
            cell = (self.x + iteration * quad_x, self.y + step * quad_y)
        return cell
    
    def _cell_in_radius(self, cell):
        cell_distance = np.sqrt((self.x - cell[0]) * (self.x - cell[0]) +
                                  (self.y - cell[1]) * (self.y - cell[1]))
        return cell_distance <= float(self.radius) + self.RADIUS_FUDGE
    
    def _cell_is_visible(self, cell_angles, obstructions):
        near_visible = True
        center_visible = True
        far_visible = True

        for obstruction in obstructions:
            if self.VISIBLE_ON_EQUAL:
                if obstruction.near < cell_angles.near < obstruction.far:
                    near_visible = False
                if obstruction.near < cell_angles.center < obstruction.far:
                    center_visible = False
                if obstruction.near < cell_angles.far < obstruction.far:
                    far_visible = False
            else:
                if obstruction.near <= cell_angles.near <= obstruction.far:
                    near_visible = False
                if obstruction.near <= cell_angles.center <= obstruction.far:
                    center_visible = False
                if obstruction.near <= cell_angles.far <= obstruction.far:
                    far_visible = False

        if self.RESTRICTIVENESS == 0:
            return center_visible or near_visible or far_visible
        elif self.RESTRICTIVENESS == 1:
            return (center_visible and near_visible) or (center_visible and far_visible)
        else:
            return center_visible and near_visible and far_visible
    
    def _add_obstruction(self, obstructions, new_obstruction):
        new_object = CellAngles(new_obstruction.near, new_obstruction.center, new_obstruction.far)
        new_list = [o for o in obstructions if not self._combine_obstructions(o, new_object)]
        new_list.append(new_object)
        return new_list
    
    def _combine_obstructions(self, old, new):
        # Pseudo-sort; if their near values are equal, they overlap
        if old.near < new.near:
            low = old
            high = new
        elif new.near < old.near:
            low = new
            high = old
        else:
            new.far = max(old.far, new.far)
            return True

        # If they overlap, combine and return True
        if low.far >= high.near:
            new.near = min(low.near, high.near)
            new.far = max(low.far, high.far)
            return True

        return False