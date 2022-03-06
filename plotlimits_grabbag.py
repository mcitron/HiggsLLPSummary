from plothelper import *

setStyle()

       
def decayMode(sample,mass):
    if "csc"  in sample: return "X#rightarrow#tau#tau"
    elif "sc" in sample and mass==40: return "#it{B}(X#rightarrow#mu#mu)=0.13"  
    elif "sc" in sample and mass==2 : return "#it{B}(X#rightarrow#mu#mu)=0.24"  
    elif "dm" in sample and mass==20 : return "#it{B}(X#rightarrow#mu#mu)=0.14" 
    elif "dm" in sample and mass==40 : return "#it{B}(X#rightarrow#mu#mu)=0.13"
    elif "dl" in sample: return "X#rightarrowee/#mu#mu"
    elif "dj" in sample: return "X#rightarrowdd"
    elif "zh" in sample: return "X#rightarrowbb"
    return ""

def plotHiggsLimits(opt="low"):
    # specify samples, and which mass/decay corresponding to sample i
    samples = ["dl","sc","dm","zh","dj","csc"]
    decays  = ["ll","mm","mm","bb","dd","tt" ]
    if opt=="high":
        masses  = [50,40,40,55,55,55 ]
    else :               
        masses  = [30,2 ,20,15,15,7 ]

    # setup plotting
    c = ROOT.TCanvas("c","",1300,900)
    
    # margins 
    left,right,top,bottom=0.15,0.28,0.08,0.15
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
    latex1.SetTextAlign(11);#xy specifies left,center
    latex1.SetTextFont(font);#same as leg
    latex2 = ROOT.TLatex() # for analysis arxiv
    latex2.SetNDC(1)
    latex2.SetTextSize(legtxt);
    latex2.SetTextAlign(11);#xy specifies left,center
    latex2.SetTextFont(font);#same as leg

    # will make different legends for each graph
    # to account for any missing samples
    dx = 0.1#(1-left-right-0.1)#/len(samples) # size of legends in x 
    x = 1-right +0.01 # x start of legend 
    dy_leg   = legtxt*1.3 #size of legend in y 
    dy_misc = dy_leg*0.6 # misc padding btw leg and decay mode
    dy_decay  = dy_leg*1.0 #dy between decay mode and arxiv 
    dy_arxiv = dy_leg*1.0 #dy between arxiv and title(legend) 
    y_start = 1-top #-0.1*dy_leg # start of first title in y
    
    # get graphs and legends 
    graphs = []
    labels = []
    legends = []
    y=y_start
    for i,sample in enumerate(samples): 
        graph=getGraph(sample,masses[i],decays[i]) 
        if graph==-1:  continue
        graph.SetLineStyle(1)
        mgraph.Add(graph)
        leg = ROOT.TLegend(x,y-dy_leg,x+dx,y)
        leg.SetBorderSize(0)
        leg.SetTextSize(legtxt+0.005)
        leg.AddEntry(graph,pretty_sample(sample),"l") 
        legends.append(leg)
        y-=dy_leg # update y
        y-=dy_misc
        y-=dy_decay
        y-=dy_arxiv
        #y-=dy_title 


    mgraph.Draw("AL")
    mgraph.SetTitle(";c#tau_{X} [mm];95% CL upper limit on #it{B}(h#rightarrowXX)")

    # draw legends and title/arxiv text
    k = 0    
    y=y_start
    dx1 = 0.025
    for i,sample in enumerate(samples):
        legends[k].Draw()
        y = y-dy_leg
        y-=dy_misc
        latex2.DrawLatex(x+dx1,y,decayMode(sample,masses[i])+", m_{X}=%i GeV"%masses[i])
        y-=dy_decay
        latex2.DrawLatex(x+dx1,y,arxiv(sample))
        y-=dy_arxiv
        graph=getGraph(sample,masses[i],decays[i]) 
        if graph==-1:continue
        #legends[k].Draw()
        #latex2.DrawLatex(x+dx/2.+dx1,y,"m_{S}=%i GeV"%masses[i])
        k+=1
        #for j,mass in enumerate(masses):
        #    graph=getGraph(sample,masses[i],decays[i]) 
        #    if graph==-1:continue
        #    y = y-dy_leg
        #    legends[k].Draw()
        #    k+=1
        #y-=dy_title 

    # Decay mode top right
    latex = ROOT.TLatex() 
    latex.SetNDC(1)
    latex.SetTextSize(0.05);
    latex.SetTextAlign(12);
    latex.SetTextFont(font);#same as leg
    #latex.DrawLatex(0.6,0.35,"h#rightarrowss")
    #latex.DrawLatex(0.55,1-top-0.05,"h#rightarrowss#rightarrow{}".format(decay_txt))

    # CMS label top left
    x,y=left+0.01,1-top+0.03
    drawCMS(x,y,dx=0.08)

    # Date
    x=0.55 #left+0.02
    y=1-top+0.03
    drawDate(x,y)

    # Luminosity & Energy
    #drawLumi(0.43,y)

    # lines
    minx,maxx,miny,maxy=5e-2,1.5e7,5e-6,1e0
    y_lines = [1e-1,1e-2,1e-3,1e-4,1e-5]
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


    c.Print("plots/higgs_llps_all_m{}_{}.pdf".format(opt,datestr))
    c.Print("plots/higgs_llps_all_m{}_{}.png".format(opt,datestr))


plotHiggsLimits("high")
plotHiggsLimits("low")
