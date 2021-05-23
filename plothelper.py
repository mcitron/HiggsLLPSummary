import ROOT
from array import array

# Define a special line
ROOT.gStyle.SetLineStyleString(11,"40 20");

# Colors - colorblind friendly
colors=[]
one   = ROOT.TColor(2001, 211/255.,93/255.,26/255.)
two   = ROOT.TColor(2002, 171/255.,73/255.,171/255.)
three = ROOT.TColor(2003, 71/255.,170/255.,173/255.)
colors.append(2001)#
colors.append(2002)#
colors.append(2003)#

# For plotting
date = "May 2021"
lumi = "117-137 fb^{-1} (13 TeV)" 
# csc = 137
# dj  = 132
# zh  = 117

def drawCMS(x,y,dx=0.1,size=0.05):
    latex = ROOT.TLatex() 
    latex.SetNDC(1)
    latex.SetTextSize(size);
    latex.SetTextAlign(12);
    latex.SetTextFont(62);#bold
    latex.DrawLatex(x,y,"CMS")

    latex = ROOT.TLatex() 
    latex.SetNDC(1)
    latex.SetTextSize(size);
    latex.SetTextAlign(12);
    latex.SetTextFont(52);#italic
    latex.DrawLatex(x+dx,y-0.005,"Preliminary")

    return

def drawDate(x,y,size=0.05,font=42):
    latex = ROOT.TLatex() 
    latex.SetNDC(1)
    latex.SetTextSize(size);
    latex.SetTextAlign(12);
    latex.SetTextFont(font);#same as leg
    latex.DrawLatex(x,y,date)
    return

def drawLumi(x,y,size=0.05,font=42):
    latex = ROOT.TLatex() 
    latex.SetNDC(1)
    latex.SetTextSize(size);
    latex.SetTextAlign(12);
    latex.SetTextFont(font);#same as leg
    latex.DrawLatex(x,y,lumi)
    return

def setStyle():
    ROOT.gROOT.SetBatch(ROOT.kTRUE)
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetOptFit(0)
    ROOT.gStyle.SetLabelFont(42,"xyz")
    ROOT.gStyle.SetLabelSize(0.05,"xyz")
    ROOT.gStyle.SetTitleFont(42,"xyz")
    ROOT.gStyle.SetTitleFont(42,"t")
    ROOT.gStyle.SetTitleSize(0.05,"xyz")
    ROOT.gStyle.SetTitleSize(0.05,"t")

    ROOT.gStyle.SetPadBottomMargin(0.14)
    ROOT.gStyle.SetPadLeftMargin(0.14)

    ROOT.gStyle.SetPadGridX(0)
    ROOT.gStyle.SetPadGridY(0)
    ROOT.gStyle.SetPadTickX(1)
    ROOT.gStyle.SetPadTickY(1)

    ROOT.gStyle.SetTitleOffset(1,'y')
    ROOT.gStyle.SetLegendTextSize(0.04)
    ROOT.gStyle.SetGridStyle(3)
    ROOT.gStyle.SetGridColor(14)

    ROOT.gStyle.SetMarkerSize(1.0) #large markers
    ROOT.gStyle.SetHistLineWidth(2) # bold lines
    ROOT.gStyle.SetLineStyleString(2,"[12 12]") # postscript dashes

    return       

