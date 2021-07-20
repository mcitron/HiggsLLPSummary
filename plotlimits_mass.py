from plothelper import *

setStyle()

def decayLabel(decay):
    if decay == "dd" : return "dd"
    if decay == "bb" : return "bb"
    if decay == "tt" : return "#tau#tau"
    else : return ""
       
def decayCosmetic(gr):
    name = gr.GetName()
    print(name)
    if "dd" in name: gr.SetLineStyle(1)
    if "bb" in name: gr.SetLineStyle(11)
    if "tt" in name: gr.SetLineStyle(2)
    return

def plotHiggsLimits(mass=15, decays=["dd","bb","tt"], samples=["zh","dj","csc"]):

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
    y_start = 1-top-1.7*dy_leg # start of first title in y
    
    # get graphs and legends 
    graphs = []
    labels = []
    legends = []
    y=y_start
    for i,sample in enumerate(samples): 
        y-=dy_arxiv
        y-=dy_lumi
        y-=dy_misc
        for j,decay in enumerate(decays):
            graph=getGraph(sample,mass,decay) 
            if graph==-1:  continue
            decayCosmetic(graph)
            mgraph.Add(graph)
            leg = ROOT.TLegend(x,y-dy_leg,x+dx,y)
            leg.SetBorderSize(0)
            leg.SetTextSize(legtxt)
            leg.AddEntry(graph,"#it{B}(s#rightarrow"+decayLabel(decay)+")=1","l")
            #leg.AddEntry(graph,"m_{s} = %i GeV"%mass,"l")
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
        for j,decay in enumerate(decays):
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
    latex.DrawLatex(0.58,0.35,"m_{s}=%i GeV"%(mass))

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


    c.Print("plots/hHad_mass{}.pdf".format(mass))
    c.Print("plots/hHad_mass{}.png".format(mass))


plotHiggsLimits(15)
plotHiggsLimits(40)
plotHiggsLimits(55)
