#!/usr/bin/env python
# coding=utf-8
#
# Copyright (C) [2021] [Pablo Andrés Díaz], [pabloandi@gmail.com]
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
"""
Scales a shoe pattern base size to others shoe sizes 
"""

from inkex import (
    EffectExtension, AbortExtension, Transform, TextElement, Group
)

class ShoePatternScaling(EffectExtension):
    """ShoePatternScaling"""
    def add_arguments(self, pars):
        pars.add_argument("--fromSize", type=int, help="Escalar desde la talla")
        pars.add_argument("--toSize", type=int, help="Escalar hasta la talla")
        pars.add_argument("--patternSize", type=int, help="Talla del patrón base")

    def effect(self):

        if len(self.svg.selection) != 1:
            raise AbortExtension(_("Debe seleccionar un objeto"))

        scale = self.svg.unittouu('1mm')  # convert to document units

        patternSize = self.options.patternSize
        fromSize = self.options.fromSize
        toSize = self.options.toSize

        if not ( fromSize <= patternSize <= toSize ):
            raise AbortExtension(_("La talla del patrón debe estar dentro de desde y hasta"))

        downerSizesCount = patternSize - fromSize
        upperSizesCount = toSize - patternSize

        
        pattern = self.svg.selection.first()
        parent = pattern.getparent()

        bbox = pattern.shape_box()
        scaleX = 10 * scale # scale width 10mm
        scaleY = 23.21 * scale # scale height 23.21mm
        width = bbox.width * scale
        height = bbox.height * scale

        for i,size in enumerate(range(patternSize + upperSizesCount, patternSize, -1)):
            copy = pattern.duplicate()
            size_text = TextElement()

            proportionX = 1 + ( 1 - ((width - (scaleX * (upperSizesCount - i))) / width))
            proportionY = 1 + ( 1 - ((height - (scaleY * (upperSizesCount - i))) / height))

            transform = Transform()
            transform.add_scale(proportionX, proportionY)
            copy.transform = transform

            size_text.text = str(size)
            size_text.set('style',"font-size:8px;shape-inside:url(#{});".format(copy.get('id')))

            group = Group()
            group.append(copy)
            group.append(size_text)
            parent.append(group)

            group.set('transform',"translate(-{},-{})".format(copy.shape_box().left, copy.shape_box().top))
        
        for i,size in enumerate(range(patternSize - 1, patternSize - downerSizesCount - 1, -1), 1):
            copy = pattern.duplicate()
            size_text = TextElement()

            proportionX = (width - (scaleX * i)) / width
            proportionY = (height - (scaleY * i)) / height


            transform = Transform()
            transform.add_scale(proportionX, proportionY)
            copy.transform = transform

            size_text.text = str(size)
            size_text.set('style',"font-size:8px;shape-inside:url(#{});".format(copy.get('id')))

            group = Group()
            group.append(copy)
            group.append(size_text)
            parent.append(group)

            group.set('transform',"translate(-{},-{})".format(copy.shape_box().left, copy.shape_box().top))


        patternGroup = Group()        
        pattern_size_text = TextElement()
        pattern_size_text.text = str(patternSize)
        pattern_size_text.set('style',"font-size:8px;shape-inside:url(#{});".format(pattern.get('id')))
        patternGroup.append(pattern)
        patternGroup.append(pattern_size_text)
        parent.append(patternGroup)
        

if __name__ == '__main__':
    ShoePatternScaling().run()
