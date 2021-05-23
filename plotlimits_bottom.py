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
    gr = removeUnphysicalXS(gr)
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
       
def plotHiggsLimits(decay="bb",masses=[15,40,55], samples=["zh","dj","csc"]):

    # setup plotting
    c = ROOT.TCanvas("c","",1000,900)
    
    # margins 
    left,right,top,bottom=0.2,0.05,0.08,0.15
    c.SetLeftMargin(left)
    c.SetRightMargin(right)
    c.SetTopMargin(top)
    c.SetBottomMargin(bottom)
    
    mgraph = ROOT.TMultiGraph()

    #  different legends for different samples
    legtxt=0.03
    dx = (1-left-right-0.1)/len(samples) # size of legends in x 
    x = [left+0.05+s*dx for s in range(0,len(samples))]
    #x = [0.27, 0.49, 0.72] # automate this
    y = 0.3
    dy=0.005+(0.01+legtxt)*len(masses)
    
    # get graphs and labels 
    graphs = []
    labels = []
    legends = []
    for i,sample in enumerate(samples): 
        leg = ROOT.TLegend(x[i],y-dy,x[i]+dx,y)
        leg.SetBorderSize(0)
        leg.SetTextSize(legtxt)
        for mass in masses:
            graph=getGraph(sample,mass,decay) 
            if graph==-1:
                # add fake graph to leg
                # maintain symmetry!
                gr_fake=ROOT.TGraph()
                gr_fake.SetLineColor(ROOT.kWhite)
                leg.AddEntry(gr_fake,"")
                continue
            mgraph.Add(graph)
            leg.AddEntry(graph,"m_{s} = %i GeV"%mass,"l")

        legends.append(leg)
        

    mgraph.Draw("AL")
    mgraph.SetTitle(";c#tau_{s} [mm];95% CL upper limit on #it{B}(h#rightarrowss)")

    #
    # handle legends and extra text here
    #
    font=42
    latex1 = ROOT.TLatex() 
    latex1.SetNDC(1)
    latex1.SetTextSize(legtxt+0.005);
    latex1.SetTextAlign(22);
    latex1.SetTextFont(font);#same as leg
    latex2 = ROOT.TLatex() 
    latex2.SetNDC(1)
    latex2.SetTextSize(legtxt);
    latex2.SetTextAlign(22);#xy specifies center
    latex2.SetTextFont(font);#same as leg
    for i,sample in enumerate(samples):
        legends[i].Draw()
        latex1.DrawLatex(x[i]+dx/2.,y+0.06,pretty_sample(sample))
        latex2.DrawLatex(x[i]+dx/2.,y+0.02,arxiv(sample))

    # Decay mode top right
    x,y=0.73,0.55
    latex = ROOT.TLatex() 
    latex.SetNDC(1)
    latex.SetTextSize(0.05);
    latex.SetTextAlign(12);
    latex.SetTextFont(font);#same as leg
    decay_txt = "4b" if decay=="bb" else "4d"
    latex.DrawLatex(x,y,"h#rightarrowss#rightarrow{}".format(decay_txt))
    #latex.DrawLatex(0.7,1-top-0.05,"h#rightarrowss#rightarrow{}".format(decay_txt))

    # Date below decay mode
    drawDate(x+0.01,y-0.06)

    # CMS label top left
    x,y=left+0.01,1-top+0.04
    drawCMS(x,y)

    # Luminosity & Energy
    drawLumi(0.56,y)

    # lines
    minx,maxx,miny,maxy=5e-1,1.5e7,2e-5,1e0
    y_lines = [1,1e-1,1e-2,1e-3]
    for y_line in y_lines: 
        lin = ROOT.TLine(minx,y_line,maxx,y_line) # BR=1
        lin.SetLineStyle(2)
        lin.SetLineColor(ROOT.kGray)
        lin.DrawLine(minx,y_line,maxx,y_line)

    # Indicate BR=1 is physical boundary 
    gr_unphys = ROOT.TGraph(2,array('d',[minx,maxx]),array('d',[1.,1.]));
    gr_unphys.SetLineColor(ROOT.kGray+1);
    gr_unphys.SetFillColor(ROOT.kGray);
    gr_unphys.SetLineWidth(300);
    gr_unphys.SetFillStyle(3553);
    #gr_unphys.Draw("same")

    latex = ROOT.TLatex() 
    latex.SetNDC(1)
    latex.SetTextSize(0.02);
    latex.SetTextColor(ROOT.kGray+1);
    latex.SetTextColor(ROOT.kGray);
    latex.SetTextAlign(12);
    latex.SetTextFont(font);#same as leg
    #latex.DrawLatex(0.76,0.54,"#it{B}=1, Physical Boundary")

    c.SetLogy(1)
    c.SetLogx(1)
    ROOT.gPad.Modified()
    mgraph.GetHistogram().GetXaxis().SetLimits(minx,maxx)
    mgraph.GetHistogram().GetYaxis().SetRangeUser(miny,maxy)
    mgraph.GetHistogram().GetYaxis().SetTitleOffset(1.4)
    mgraph.GetHistogram().GetXaxis().SetTitleOffset(1.3)
    c.Update()

    c.Print("h{}_bottom.pdf".format(decay_txt))
    c.Print("h{}_bottom.png".format(decay_txt))


plotHiggsLimits("bb")
plotHiggsLimits("dd")
