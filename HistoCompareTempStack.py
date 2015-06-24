import ROOT as r
import glob

parameters = {}
parameters['NoiseROC'] = dict(file='NoiseROC', canvas = 'Mean Noise per ROC', xaxistitle = 'Mean Noise [e^{-}]', gradB = 500, gradC = 1000)
parameters['Noise'] = dict(file='NoiseDistr', canvas = 'Noise distribution', xaxistitle = 'Noise [e^{-}]', gradB = 50, gradC = 400)
parameters['RelativeGainWidth'] = dict(file='RelativeGainWidth', canvas = 'Relative Gain Width', xaxistitle = 'Relative Gain Width', gradB = 0.1, gradC = 0.2)
parameters['VcalThresholdWidth'] = dict(file='VcalThresholdWidth', canvas = 'Vcal Threshold Width', xaxistitle = 'Width of Vcal Threshold [e^{-}]', gradB = 200, gradC = 400)
parameters['PHCalibrationParameter1'] = dict(file='PHCalibrationParameter1', canvas = 'PH Calibration Parameter1', xaxistitle = 'Parameter 1', gradB = 0, gradC = 2)
parameters['PedestalSpread'] = dict(file='PedestalSpread', canvas = 'Pedestal Spread', xaxistitle = 'Average Pedestal [e^{-}]', gradB = 2500, gradC = 5000)
#Only in case the current is measured at -20C:
parameters['Current150V'] = dict(file='Current150V', canvas = 'Current at Voltage 150V', xaxistitle = 'Leakage current at 150V [microA]', gradB = 3, gradC = 15)
parameters['SlopeIV'] = dict(file='SlopeIV', canvas = 'Slope IV', xaxistitle = 'Slope IV [microA]', gradB = 400, gradC = 2)



def main():
   for par in parameters.keys():
      #FilePathm20 = GetFilePath('m20')
      #FilePathp17 = GetFilePath('p17')
      Filem20 = r.TFile('m20'+parameters[par]['file']+'.root')
      cFilem20 = Filem20.Get(parameters[par]['canvas']+'m20')
      Listm20 = cFilem20.GetListOfPrimitives()
      histom20 = Listm20[1]
      Filep17 = r.TFile('p17'+parameters[par]['file']+'.root')
      cFilep17 = Filep17.Get(parameters[par]['canvas']+'p17')
      Listp17 = cFilep17.GetListOfPrimitives()
      histop17 = Listp17[1]
      histom20.SetName('m20')
      histop17.SetName('p17')
      canvas = r.TCanvas(parameters[par]['canvas'], "", 1)
      canvas.cd()
      canvas.SetLogy()
      stack = r.THStack('stack', parameters[par]['canvas'])
      histom20.SetLineColor(38)
      histop17.SetLineColor(46)
      histom20.SetFillColor(38)
      histop17.SetFillColor(46)
      stack.Add(histom20)
      stack.Add(histop17)
      histom20.SetStats(0)
      histop17.SetStats(0)
      max = stack.GetMaximum()
      stack.SetMaximum(max*10)
      stack.SetMinimum(0.5)
      stack.Draw()
      if par == 'Noise' or par == 'PHCalibrationParameter1':
         stack.GetYaxis().SetTitle('# Pixels')
      elif par == 'Current150V' or par == 'SlopeIV':
         stack.GetYaxis().SetTitle('# Modules')
      else:
         stack.GetYaxis().SetTitle('# ROCs')
      stack.GetXaxis().SetTitle(parameters[par]['xaxistitle'])
      r.gPad.Update()
      gradB = r.TLine(parameters[par]['gradB'], 0, parameters[par]['gradB'], max*5)
      gradC = r.TLine(parameters[par]['gradC'], 0, parameters[par]['gradC'], max*5)
      gradB.SetLineColor(r.kOrange)
      if par == 'Noise' or par == 'PHCalibrationParameter1':
         gradC.SetLineColor(r.kOrange)
      else:
         gradC.SetLineColor(r.kRed)
      gradB.SetLineStyle(2)
      gradC.SetLineStyle(2)
      gradB.SetLineWidth(3)
      gradC.SetLineWidth(3)
      gradB.Draw()
      gradC.Draw()
      latex = r.TLatex()
      latex.SetNDC()
      latex.SetTextAlign(13)
      latex.DrawLatex(0.2, 0.87, '#color[38]{N: '+'{:.0f}'.format(histom20.GetEntries())+'  Mean: '+'{:.3f}'.format(histom20.GetMean())+'  RMS: '+'{:.3f}'.format(histom20.GetRMS())+'}')
      latex.DrawLatex(0.2, 0.82, '#color[46]{N: '+'{:.0f}'.format(histop17.GetEntries())+'  Mean: '+'{:.3f}'.format(histop17.GetMean())+'  RMS: '+'{:.3f}'.format(histop17.GetRMS())+'}')
      Legend = r.TLegend(0.5,0.55,0.73,0.75)
      Legend.AddEntry('p17', 'Fulltest at 17 C', 'f')
      Legend.AddEntry('m20', 'Fulltest at -20 C', 'f')
      Legend.SetBorderSize(0)
      #Legend.AddEntry('gradB', 'Grade B threshold', 'l')
      #Legend.AddEntry('gradC', 'Grade C threshold', 'l')
      Legend.Draw()
      for fmt in ['.root', '.png', '.pdf']:
         canvas.SaveAs(parameters[par]['file']+str(fmt))




main()
