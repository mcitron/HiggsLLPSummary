import ROOT
from array import array
from ctypes import c_double

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
date    = "March 2022"
datestr = "March_2022"

# Input files here
# get files
f_zh_4b  = ROOT.TFile.Open("input/exo_20_003_4b_obs_exp.root")
f_zh_4d  = ROOT.TFile.Open("input/exo_20_003_4d_obs_exp.root")
f_dj_4b  = ROOT.TFile.Open("input/ggHbbbb_limits.root")
f_dj_4d  = ROOT.TFile.Open("input/ggHdddd_limits.root")
f_csc    = ROOT.TFile.Open("input/limits_exo_20_015.root")
f_dl     = ROOT.TFile.Open("input/limit_plot_BR_mm.root")
f_sc     = ROOT.TFile.Open("input/upperlimit_br_H4_vsctau.root")
f_dm_20     = ROOT.TFile.Open("input/EXO-21-006_obs_20.root")
f_dm_40     = ROOT.TFile.Open("input/EXO-21-006_obs_40.root")

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


def removeUnphysicalXS(graph):
    name = graph.GetName()
    n = graph.GetN()
    ct = []
    xs = []
    for i in range(0,n): 
        x,y=ROOT.Double(0.), ROOT.Double(0.)
        graph.GetPoint(i,x,y)
        if y<1: 
            ct.append( x )
            xs.append( y )
        
    graph_clean = ROOT.TGraph(len(ct),array("d",ct),array("d",xs))
    graph_clean.SetName(name+"_clean")
    return graph_clean

def convert_cm_to_mm(graph):
    name = graph.GetName()
    n = graph.GetN()
    mm = []
    xs = []
    for i in range(0,n): 
        x,y=c_double(0.),c_double(0.)
        #x,y=ROOT.Double(0.), ROOT.Double(0.)
        graph.GetPoint(i,x,y)
        mm.append( x.value*10. )
        xs.append( y.value )
        
    graph_mm = ROOT.TGraph(len(mm),array("d",mm),array("d",xs))
    graph_mm.SetName(name+"_mm")
    return graph_mm

def convert_m_to_mm(graph):
    name = graph.GetName()
    n = graph.GetN()
    mm = []
    xs = []
    for i in range(0,n): 
        x,y=c_double(0.),c_double(0.)
        #x,y=ROOT.Double(0.), ROOT.Double(0.)
        graph.GetPoint(i,x,y)
        mm.append( x.value*1000. )
        xs.append( y.value )
        
    graph_mm = ROOT.TGraph(len(mm),array("d",mm),array("d",xs))
    graph_mm.SetName(name+"_mm")
    return graph_mm

def cosmetic(graph):
    name = graph.GetName()
    if "zh"  in name:graph.SetLineColor(ROOT.kRed-4) 
    elif "csc" in name:graph.SetLineColor(ROOT.kBlue-4)
    elif "dj"  in name:graph.SetLineColor(ROOT.kTeal+2) 
    elif "dl"  in name:graph.SetLineColor(ROOT.kOrange+1)
    elif "sc"  in name:graph.SetLineColor(ROOT.kMagenta+1)
    elif "dm"  in name:graph.SetLineColor(ROOT.kAzure-4)
    graph.SetMarkerSize(0)
    graph.SetLineWidth(3)
    if "15" in name: graph.SetLineStyle(2)
    elif "40" in name: graph.SetLineStyle(11)
    elif "55" in name: graph.SetLineStyle(1)
    return  
  
def getGraph(sample, mass, decay): 
    # Get's graph from file of interest
    # Add new samples/masses/decays here
    #print(sample,mass,decay)
    gr=-1
    if sample=="zh" : 
        if decay=="bb"   : gr = f_zh_4b.Get("gObs_{}".format(mass)) 
        elif decay == "tt" : gr=-1
        elif decay=="dd" : gr = f_zh_4d.Get("gObs_{}".format(mass))
    elif sample=="csc" : 
        if decay=="bb"   : gr = convert_m_to_mm( f_csc.Get("h_bbbb_m{}_obs".format(mass))) 
        elif decay=="dd" : gr = convert_m_to_mm( f_csc.Get("h_dddd_m{}_obs".format(mass))) 
        elif decay=="tt" : gr = convert_m_to_mm( f_csc.Get("h_4Tau_m{}_obs".format(mass)))
    elif sample=="dj" :
        if mass==15 and decay == "bb" : gr=-1 #shitty hack
        elif decay == "tt" : gr=-1
        elif decay=="bb" : gr = f_dj_4b.Get("gra_ggHbbbb_m{}_observed".format(mass))
        elif decay=="dd" : gr = f_dj_4d.Get("gra_ggHdddd_m{}_observed".format(mass))
    elif sample=="dl" : 
        gr = f_dl.Get("h_m_{H} = 125 GeV, m_{S} = %i GeV"%mass)
    elif sample=="sc" : 
        gr = f_sc.Get("gobs_m{}.0".format(mass))
    elif sample=="dm" : # dimuon DV
        if mass==20 : gr = convert_cm_to_mm( f_dm_20.Get("OBS_20") )
        if mass==40 : gr = convert_cm_to_mm( f_dm_40.Get("OBS_40") )

    print(sample,mass,decay)
    print(gr) 

    if gr==-1: 
        print("SAMPLE {} NOT FOUND".format(sample))
        return -1

    # cleanup
    #gr = removeUnphysicalXS(gr)
    gr.SetName("gr_{}_{}_{}".format(sample,mass,decay))
    cosmetic(gr)
    return gr 

def pretty_sample(sample):
    if sample=="zh" : return "Z + displaced jets"
    if sample=="dj" : return "Displaced jets"
    if sample=="csc": return "Hadronic MS"
    if sample=="dl" : return "Displaced leptons"
    if sample=="sc" : return "Dimuon scouting"
    if sample=="dm" : return "Displaced dimuon"
    return 

def arxiv(sample):
    if sample=="zh" : return "2110.13218" #"EXO-20-003"
    if sample=="dj" : return "2012.01581"
    if sample=="csc": return "2107.04838"
    if sample=="dl" : return "2110.04809" #"EXO-18-003"
    if sample=="sc" : return "2112.13769" #"EXO-20-014"
    if sample=="dm" : return "EXO-21-006"
    return 

def lumi(sample):
    #lumi = "117-137 fb^{-1} (13 TeV)" 
    if sample=="zh" : return "117 fb^{-1}, 13 TeV"
    if sample=="dj" : return "132 fb^{-1}, 13 TeV"
    if sample=="csc": return "137 fb^{-1}, 13 TeV"
    if sample=="dl" : return "113 fb^{-1}, 13 TeV"
    if sample=="sc" : return "101 fb^{-1}, 13 TeV"
    if sample=="dm" : return "97.6 fb^{-1}, 13 TeV"

    return 
