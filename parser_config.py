#!/usr/bin/env python
import ConfigParser,os
"""
Descripcion: Modulo que permite manipular archivos de configuracion.
Autor: Ernesto Crespo
Correo: ecrespo@gmail.com
Licencia: GPL Version 3
Copyright: Copyright (C) 2011 Ernesto Nadir Crespo Avila
Version: 0.2

"""

class config:
    """Modulo que permite manejar archivo de configuracion"""    
    def __init__(self,cnffile):
        self.__cnffile = cnffile
        self.__config = ConfigParser.ConfigParser()
        self.__config.read(self.__cnffile)
        
        
    def ShowItemSection(self,section):
        return self.__config.items(section)
    
    def ShowValueItem(self,section,option):
        return self.__config.get(section,option)
    
    def change(self,section,option,value):
        self.__config.set(section,option,value)

    
    def write(self):
        self.__config.write(open(self.__cnffile,'w'))



