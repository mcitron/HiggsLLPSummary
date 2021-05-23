from plothelper import *

setStyle()

# Input files here
# get files
f_zh_4b  = ROOT.TFile.Open("exo_20_003_4b_obs_exp.root")
f_zh_4d  = ROOT.TFile.Open("exo_20_003_4d_obs_exp.root")
f_dj_4b  = ROOT.TFile.Open("ggHbbbb_limits.root")
f_dj_4d  = ROOT.TFile.Open("ggHdddd_limits.root")
f_csc    = ROOT.TFile.Open("limits_exo_20_015.root")

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

def convert_m_to_mm(graph):
    name = graph.GetName()
    n = graph.GetN()
    mm = []
    xs = []
    for i in range(0,n): 
        x,y=ROOT.Double(0.), ROOT.Double(0.)
        graph.GetPoint(i,x,y)
        mm.append( x*1000 )
        xs.append( y )
        
    graph_mm = ROOT.TGraph(len(mm),array("d",mm),array("d",xs))
    graph_mm.SetName(name+"_mm")
    return graph_mm

def cosmetic(graph):
    name = graph.GetName()
    if "zh"  in name:graph.SetLineColor(ROOT.kRed-4) 
    if "csc" in name:graph.SetLineColor(ROOT.kBlue-4)
    if "dj"  in name:graph.SetLineColor(ROOT.kTeal+2) 
    graph.SetMarkerSize(0)
    graph.SetLineWidth(3)
    if "15" in name: graph.SetLineStyle(2)
    if "40" in name: graph.SetLineStyle(11)
    if "55" in name: graph.SetLineStyle(1)
    return  
  
def getGraph(sample, mass, decay): 
    # Get's graph from file of interest
    # Add new samples/masses/decays here
    #print(sample,mass,decay)
    gr=-1
    if sample=="zh" : 
        if decay=="bb"   : gr = f_zh_4b.Get("gObs_{}".format(mass)) 
        elif decay=="dd" : gr = f_zh_4d.Get("gObs_{}".format(mass))
    elif sample=="csc" : 
        if decay=="bb"   : gr = convert_m_to_mm( f_csc.Get("h_bbbb_m{}_obs".format(mass))) 
        elif decay=="dd" : gr = convert_m_to_mm( f_csc.Get("h_dddd_m{}_obs".format(mass))) 
    elif sample=="dj" :
        if mass==15 and decay == "bb" : gr=-1 #shitty hack
        elif decay=="bb" : gr = f_dj_4b.Get("gra_ggHbbbb_m{}_observed".format(mass))
        elif decay=="dd" : gr = f_dj_4d.Get("gra_ggHdddd_m{}_observed".format(mass))

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
    return 

def arxiv(sample):
    if sample=="zh" : return "EXO-20-003"
    if sample=="dj" : return "2012.01581"
    if sample=="csc": return "EXO-20-015"
    return 

def lumi(sample):
    #lumi = "117-137 fb^{-1} (13 TeV)" 
    if sample=="zh" : return "117 fb^{-1}, 13 TeV"
    if sample=="dj" : return "132 fb^{-1}, 13 TeV"
    if sample=="csc": return "137 fb^{-1}, 13 TeV"
    return 
       
def plotHiggsLimits(decay="bb",masses=[15,40,55], samples=["zh","dj","csc"]):

    # setup plotting
    c = ROOT.TCanvas("c","",1200,900)
    
    # margins 
    left,right,top,bottom=0.15,0.22,0.08,0.15
    c.SetLeftMargin(left)
    c.SetRightMargin(right)
    c.SetTopMargin(top)
    c.SetBottomMargin(bottom)
    
    mgraph = ROOT.TMultiGraph()

    #
    # handle legends here
    #
    font=42
    legtxt=0.03
    latex1 = ROOT.TLatex()# for analysis title 
    latex1.SetNDC(1)
    latex1.SetTextSize(legtxt+0.005);
    latex1.SetTextAlign(21);#xy specifies center
    latex1.SetTextFont(font);#same as leg
    latex2 = ROOT.TLatex() # for analysis arxiv
    latex2.SetNDC(1)
    latex2.SetTextSize(legtxt);
    latex2.SetTextAlign(21);#xy specifies center
    latex2.SetTextFont(font);#same as leg

    # will make different legends for each graph
    # to account for any missing samples
    dx = (1-left-right-0.1)/len(samples) # size of legends in x 
    x = 1-right+0.02 # x start of legend 
    dy_leg   = legtxt*1.3 #size of legend in y 
    dy_title = dy_leg*1.3 #dy between title and previous leg 
    dy_arxiv = dy_leg*1.0 #dy between title and arxiv
    dy_lumi  = dy_leg*1.0 #dy between arxiv and lumi
    dy_misc  = dy_leg*0.3 #dy between lumi and leg
    y_start = 1-top-(1.5 if decay=="bb" else 1.1)*dy_leg # start of first title in y
    
    # get graphs and legends 
    graphs = []
    labels = []
    legends = []
    y=y_start
    for i,sample in enumerate(samples): 
        y-=dy_arxiv
        y-=dy_lumi
        y-=dy_misc
        for j,mass in enumerate(masses):
            graph=getGraph(sample,mass,decay) 
            if graph==-1:  continue
            mgraph.Add(graph)
            leg = ROOT.TLegend(x,y-dy_leg,x+dx,y)
            leg.SetBorderSize(0)
            leg.SetTextSize(legtxt)
            leg.AddEntry(graph,"m_{s} = %i GeV"%mass,"l")
            legends.append(leg)
            y-=dy_leg # update y
        y-=dy_title 


    mgraph.Draw("AL")
    mgraph.SetTitle(";c#tau_{s} [mm];95% CL upper limit on #it{B}(h#rightarrowss)")

    # draw legends and title/arxiv text
    k = 0    
    y=y_start
    for i,sample in enumerate(samples):
        latex1.DrawLatex(x+dx/2.,y,pretty_sample(sample))
        y-=dy_arxiv
        latex2.DrawLatex(x+dx/2.,y,arxiv(sample))
        y-=dy_lumi
        latex2.DrawLatex(x+dx/2.,y,lumi(sample))
        y-=dy_misc
        for j,mass in enumerate(masses):
            graph=getGraph(sample,mass,decay) 
            if graph==-1:continue
            y = y-dy_leg
            legends[k].Draw()
            k+=1
        y-=dy_title 

    # Decay mode top right
    latex = ROOT.TLatex() 
    latex.SetNDC(1)
    latex.SetTextSize(0.05);
    latex.SetTextAlign(12);
    latex.SetTextFont(font);#same as leg
    decay_txt = "4b" if decay=="bb" else "4d"
    latex.DrawLatex(0.6,0.35,"h#rightarrowss#rightarrow{}".format(decay_txt))
    #latex.DrawLatex(0.55,1-top-0.05,"h#rightarrowss#rightarrow{}".format(decay_txt))

    # CMS label top left
    x,y=left+0.01,1-top+0.03
    drawCMS(x,y,dx=0.08)

    # Date
    x=0.62 #left+0.02
    y=1-top+0.03
    drawDate(x,y)

    # Luminosity & Energy
    #drawLumi(0.43,y)

    # lines
    minx,maxx,miny,maxy=5e-1,1.5e7,5e-4,1e0
    y_lines = [1e-1,1e-2,1e-3]
    #y_lines = [1,1e-1,1e-2,1e-3]
    for y_line in y_lines: 
        lin = ROOT.TLine(minx,y_line,maxx,y_line) # BR=1
        lin.SetLineStyle(2)
        lin.SetLineColor(ROOT.kGray)
        lin.DrawLine(minx,y_line,maxx,y_line)

    # Indicate BR=1 is physical boundary 
    latex = ROOT.TLatex() 
    latex.SetNDC(1)
    latex.SetTextSize(0.02);
    latex.SetTextColor(ROOT.kGray);
    latex.SetTextAlign(12);
    latex.SetTextFont(font);#same as leg
    #latex.DrawLatex(0.59,0.81,"#it{B}=1, Physical Boundary")

    gr_unphys = ROOT.TGraph(2,array('d',[minx,maxx]),array('d',[1.,1.]));
    gr_unphys.SetLineColor(ROOT.kGray+1);
    gr_unphys.SetFillColor(ROOT.kGray);
    gr_unphys.SetLineWidth(300);
    gr_unphys.SetFillStyle(3553);
    #gr_unphys.Draw("same")

    c.SetLogy(1)
    c.SetLogx(1)
    ROOT.gPad.Modified()
    mgraph.GetHistogram().GetXaxis().SetLimits(minx,maxx)
    mgraph.GetHistogram().GetYaxis().SetRangeUser(miny,maxy)
    mgraph.GetHistogram().GetYaxis().SetTitleOffset(1.3)
    mgraph.GetHistogram().GetXaxis().SetTitleOffset(1.3)
    c.Update()


    c.Print("h{}_side.pdf".format(decay_txt))
    c.Print("h{}_side.png".format(decay_txt))


plotHiggsLimits("bb")
plotHiggsLimits("dd")
