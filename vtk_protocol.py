import string
import time
import os
import logging

from numpy import array

from vtk.web import protocols as vtk_protocols

from wslink import register as exportRpc

import vtk

# -------------------------------------------------------------------------
# ViewManager
# -------------------------------------------------------------------------


class VtkView(vtk_protocols.vtkWebProtocol):
    def __init__(self):
        self.DataReader = vtk.vtkXMLPolyDataReader()
        self.ImageReader = vtk.vtkXMLImageDataReader()

    @exportRpc("create.visualization")
    def createVisualization(self):
        renderWindow = self.getView('-1')
        renderer = renderWindow.GetRenderers().GetFirstRenderer()
        renderer.SetBackground([0/255, 54/255, 48/255])

        renderer.ResetCamera()
        renderWindow.Render()

        return self.resetCamera()

    @exportRpc("reset.camera")
    def resetCamera(self):
        print("coucou2")
        renderWindow = self.getView('-1')
        renderWindow.GetRenderers().GetFirstRenderer().ResetCamera()
        renderWindow.Render()

        return -1

    @exportRpc("send.filenames")
    def sendFilenames(self, filenames):
        logging.error(filenames)
        VtiFilename = filenames['VtiFilename']
        VtpFilename = filenames['VtpFilename']
        
        DataReader = self.DataReader
        DataReader.SetFileName(f"./{VtpFilename}")


        # logging.error('lines')
        # with open(f"./{VtiFilename}") as f:
        #     lines = f.readlines()
        #     logging.error(lines)
        ImageReader = self.ImageReader
        ImageReader.SetFileName(f"./{VtiFilename}")
        texture = vtk.vtkTexture()

        texture.SetInputConnection(ImageReader.GetOutputPort())

        actor = vtk.vtkActor()
        mapper = vtk.vtkPolyDataMapper()
        actor.SetMapper(mapper)
        actor.SetTexture(texture)

        mapper.SetInputConnection(DataReader.GetOutputPort())
        renderWindow = self.getView('-1')
        renderer = renderWindow.GetRenderers().GetFirstRenderer()
        renderer.AddActor(actor)
        print("coucou1")
        renderer.ResetCamera()
        renderWindow.Render()
        self.getApplication().InvokeEvent('UpdateEvent')

    @exportRpc("update.resolution")
    def updateResolution(self, resolution):
        self.cone.SetResolution(resolution)
        renderWindow = self.getView('-1')
        renderWindow.Render()
        self.getApplication().InvokeEvent('UpdateEvent')


    @exportRpc("update.height")
    def updateHeight(self, height):
        self.cone.SetHeight(height)
        renderWindow = self.getView('-1')
        renderWindow.Render()
        self.getApplication().InvokeEvent('UpdateEvent')
    @exportRpc("geode.reset")
    def reset(self):
        # self.getDataBase().clear()
        renderWindow = self.getView('-1')
        renderWindow.GetRenderers().GetFirstRenderer().RemoveAllViewProps()
        print("reset")