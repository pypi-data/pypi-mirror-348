#List of unscaled area values and scale factors for each peak type and sigma/gamma value 

#Will need to expand to include all asymmtery values and coster-kronig values


class area_values():
    def __init__(self):

        for self.peakType in self.peaks:
            if(self.peakType.lower() == "voigt"):
                self.func = self.voigtArea
            elif(self.peakType.lower() == "gaussian"):
                self.func = self.gaussArea
            elif(self.peakType.lower() == "lorentzian"):
                self.func = self.lorentzArea
            elif(self.peakType.lower() == "double lorentzian"):
                self.func = self.doubleLorentzArea
            elif(self.peakType.lower() == "doniach-sunjic"):
                self.func = self.doniachSunjicArea

            else:
                print("Error assigning peak type")
                print("Peaktype found is: " + str(self.peakType))
                exit()

    def areaFunc(self): #Call this function to retrieve area_unscaled and scale_factor 
        #Peak Area = area_unscaled*(amp/scale)*step_size
        return self.func(self)
    

    def voigtArea(self):
        pass

    def lorentzArea(self):
        if self.gamma == 0.01:
            self.unscalred_area = 63.74545
            self.scale = 63.66198
        elif self.gamma == 0.02:
            self.unscalred_area = 31.9978
            self.scale = 31.83099
        elif self.gamma == 0.03:
            self.unscalred_area = 21.47054
            self.scale = 21.22066
        elif self.gamma == 0.04:
            self.unscalred_area = 16.24806
            self.scale = 15.91549
        elif self.gamma == 0.05:
            self.unscalred_area = 13.14713
            self.scale = 12.7324
        elif self.gamma == 0.06:
            self.unscalred_area = 11.10659
            self.scale = 10.61033
        elif self.gamma == 0.07:
            self.unscalred_area = 9.67159
            self.scale = 9.09457
        elif self.gamma == 0.08:
            self.unscalred_area = 8.61467
            self.scale = 7.95775
        elif self.gamma == 0.09:
            self.unscalred_area = 7.80939
            self.scale = 7.07355
        elif self.gamma == 0.1:
            self.unscalred_area = 7.17987
            self.scale = 6.3662
        elif self.gamma == 0.11:
            self.unscalred_area = 6.6778
            self.scale = 5.78745
        elif self.gamma == 0.12:
            self.unscalred_area = 6.27093
            self.scale = 5.30516
        elif self.gamma == 0.13:
            self.unscalred_area = 5.93693
            self.scale = 4.89708
        elif self.gamma == 0.14:
            self.unscalred_area = 5.65982
            self.scale = 4.54728
        elif self.gamma == 0.15:
            self.unscalred_area = 5.42789
            self.scale = 4.24413
        elif self.gamma == 0.16:
            self.unscalred_area = 5.23234
            self.scale = 3.97887
        elif self.gamma == 0.17:
            self.unscalred_area = 5.06644
            self.scale = 3.74482
        elif self.gamma == 0.18:
            self.unscalred_area = 4.92495
            self.scale = 3.53678
        elif self.gamma == 0.19:
            self.unscalred_area = 4.80373
            self.scale = 3.35063
        elif self.gamma == 0.2:
            self.unscalred_area = 4.69948
            self.scale = 3.1831
        elif self.gamma == 0.21:
            self.unscalred_area = 4.60952
            self.scale = 3.03152
        elif self.gamma == 0.22:
            self.unscalred_area = 4.53167
            self.scale = 2.89373
        elif self.gamma == 0.23:
            self.unscalred_area = 4.46413
            self.scale = 2.76791
        elif self.gamma == 0.24:
            self.unscalred_area = 4.40541
            self.scale = 2.65258
        elif self.gamma == 0.25:
            self.unscalred_area = 4.35425
            self.scale = 2.54648
        elif self.gamma == 0.26:
            self.unscalred_area = 4.30961
            self.scale = 2.44854
        elif self.gamma == 0.27:
            self.unscalred_area = 4.2706
            self.scale = 2.35785
        elif self.gamma == 0.28:
            self.unscalred_area = 4.23645
            self.scale = 2.27364
        elif self.gamma == 0.29:
            self.unscalred_area = 4.20654
            self.scale = 2.19524
        elif self.gamma == 0.3:
            self.unscalred_area = 4.1803
            self.scale = 2.12207
        elif self.gamma == 0.31:
            self.unscalred_area = 4.15726
            self.scale = 2.05361
        elif self.gamma == 0.32:
            self.unscalred_area = 4.13701
            self.scale = 1.98944
        elif self.gamma == 0.33:
            self.unscalred_area = 4.1192
            self.scale = 1.92915
        elif self.gamma == 0.34:
            self.unscalred_area = 4.10353
            self.scale = 1.87241
        elif self.gamma == 0.35:
            self.unscalred_area = 4.08971
            self.scale = 1.81891
        elif self.gamma == 0.36:
            self.unscalred_area = 4.07754
            self.scale = 1.76839
        elif self.gamma == 0.37:
            self.unscalred_area = 4.0668
            self.scale = 1.72059
        elif self.gamma == 0.38:
            self.unscalred_area = 4.05731
            self.scale = 1.67532
        elif self.gamma == 0.39:
            self.unscalred_area = 4.04893
            self.scale = 1.63236
        elif self.gamma == 0.4:
            self.unscalred_area = 4.04152
            self.scale = 1.59155
        elif self.gamma == 0.41:
            self.unscalred_area = 4.03496
            self.scale = 1.55273
        elif self.gamma == 0.42:
            self.unscalred_area = 4.02915
            self.scale = 1.51576
        elif self.gamma == 0.43:
            self.unscalred_area = 4.024
            self.scale = 1.48051
        elif self.gamma == 0.44:
            self.unscalred_area = 4.01943
            self.scale = 1.44686
        elif self.gamma == 0.45:
            self.unscalred_area = 4.01537
            self.scale = 1.41471
        elif self.gamma == 0.46:
            self.unscalred_area = 4.01176
            self.scale = 1.38396
        elif self.gamma == 0.47:
            self.unscalred_area = 4.00854
            self.scale = 1.35451
        elif self.gamma == 0.48:
            self.unscalred_area = 4.00567
            self.scale = 1.32629
        elif self.gamma == 0.49:
            self.unscalred_area = 4.00311
            self.scale = 1.29922
        elif self.gamma == 0.5:
            self.unscalred_area = 4.00082
            self.scale = 1.27324
        elif self.gamma == 0.51:
            self.unscalred_area = 3.99877
            self.scale = 1.24827
        elif self.gamma == 0.52:
            self.unscalred_area = 3.99692
            self.scale = 1.22427
        elif self.gamma == 0.53:
            self.unscalred_area = 3.99526
            self.scale = 1.20117
        elif self.gamma == 0.54:
            self.unscalred_area = 3.99377
            self.scale = 1.17893
        elif self.gamma == 0.55:
            self.unscalred_area = 3.99242
            self.scale = 1.15749
        elif self.gamma == 0.56:
            self.unscalred_area = 3.99119
            self.scale = 1.13682
        elif self.gamma == 0.57:
            self.unscalred_area = 3.99008
            self.scale = 1.11688
        elif self.gamma == 0.58:
            self.unscalred_area = 3.98906
            self.scale = 1.09762
        elif self.gamma == 0.59:
            self.unscalred_area = 3.98813
            self.scale = 1.07902
        elif self.gamma == 0.6:
            self.unscalred_area = 3.98728
            self.scale = 1.06103
        elif self.gamma == 0.61:
            self.unscalred_area = 3.98649
            self.scale = 1.04364
        elif self.gamma == 0.62:
            self.unscalred_area = 3.98577
            self.scale = 1.02681
        elif self.gamma == 0.63:
            self.unscalred_area = 3.98509
            self.scale = 1.01051
        elif self.gamma == 0.64:
            self.unscalred_area = 3.98446
            self.scale = 0.99472
        elif self.gamma == 0.65:
            self.unscalred_area = 3.98388
            self.scale = 0.97942
        elif self.gamma == 0.66:
            self.unscalred_area = 3.98333
            self.scale = 0.96458
        elif self.gamma == 0.67:
            self.unscalred_area = 3.98281
            self.scale = 0.95018
        elif self.gamma == 0.68:
            self.unscalred_area = 3.98232
            self.scale = 0.93621
        elif self.gamma == 0.69:
            self.unscalred_area = 3.98185
            self.scale = 0.92264
        elif self.gamma == 0.7:
            self.unscalred_area = 3.9814
            self.scale = 0.90946
        elif self.gamma == 0.71:
            self.unscalred_area = 3.98098
            self.scale = 0.89665
        elif self.gamma == 0.72:
            self.unscalred_area = 3.98057
            self.scale = 0.88419
        elif self.gamma == 0.73:
            self.unscalred_area = 3.98018
            self.scale = 0.87208
        elif self.gamma == 0.74:
            self.unscalred_area = 3.97979
            self.scale = 0.8603
        elif self.gamma == 0.75:
            self.unscalred_area = 3.97943
            self.scale = 0.84883
        elif self.gamma == 0.76:
            self.unscalred_area = 3.97907
            self.scale = 0.83766
        elif self.gamma == 0.77:
            self.unscalred_area = 3.97872
            self.scale = 0.82678
        elif self.gamma == 0.78:
            self.unscalred_area = 3.97837
            self.scale = 0.81618
        elif self.gamma == 0.79:
            self.unscalred_area = 3.97804
            self.scale = 0.80585
        elif self.gamma == 0.8:
            self.unscalred_area = 3.97771
            self.scale = 0.79577
        elif self.gamma == 0.81:
            self.unscalred_area = 3.97739
            self.scale = 0.78595
        elif self.gamma == 0.82:
            self.unscalred_area = 3.97707
            self.scale = 0.77637
        elif self.gamma == 0.83:
            self.unscalred_area = 3.97675
            self.scale = 0.76701
        elif self.gamma == 0.84:
            self.unscalred_area = 3.97644
            self.scale = 0.75788
        elif self.gamma == 0.85:
            self.unscalred_area = 3.97613
            self.scale = 0.74896
        elif self.gamma == 0.86:
            self.unscalred_area = 3.97583
            self.scale = 0.74026
        elif self.gamma == 0.87:
            self.unscalred_area = 3.97553
            self.scale = 0.73175
        elif self.gamma == 0.88:
            self.unscalred_area = 3.97523
            self.scale = 0.72343
        elif self.gamma == 0.89:
            self.unscalred_area = 3.97493
            self.scale = 0.7153
        elif self.gamma == 0.9:
            self.unscalred_area = 3.97463
            self.scale = 0.70736
        elif self.gamma == 0.91:
            self.unscalred_area = 3.97434
            self.scale = 0.69958
        elif self.gamma == 0.92:
            self.unscalred_area = 3.97405
            self.scale = 0.69198
        elif self.gamma == 0.93:
            self.unscalred_area = 3.97375
            self.scale = 0.68454
        elif self.gamma == 0.94:
            self.unscalred_area = 3.97346
            self.scale = 0.67726
        elif self.gamma == 0.95:
            self.unscalred_area = 3.97317
            self.scale = 0.67013
        elif self.gamma == 0.96:
            self.unscalred_area = 3.97288
            self.scale = 0.66315
        elif self.gamma == 0.97:
            self.unscalred_area = 3.9726
            self.scale = 0.65631
        elif self.gamma == 0.98:
            self.unscalred_area = 3.97231
            self.scale = 0.64961
        elif self.gamma == 0.99:
            self.unscalred_area = 3.97202
            self.scale = 0.64305
        elif self.gamma == 1.0:
            self.unscalred_area = 3.97173
            self.scale = 0.63662
        elif self.gamma == 1.01:
            self.unscalred_area = 3.97145
            self.scale = 0.63032
        elif self.gamma == 1.02:
            self.unscalred_area = 3.97116
            self.scale = 0.62414
        elif self.gamma == 1.03:
            self.unscalred_area = 3.97088
            self.scale = 0.61808
        elif self.gamma == 1.04:
            self.unscalred_area = 3.97059
            self.scale = 0.61213
        elif self.gamma == 1.05:
            self.unscalred_area = 3.97031
            self.scale = 0.6063
        elif self.gamma == 1.06:
            self.unscalred_area = 3.97002
            self.scale = 0.60058
        elif self.gamma == 1.07:
            self.unscalred_area = 3.96974
            self.scale = 0.59497
        elif self.gamma == 1.08:
            self.unscalred_area = 3.96945
            self.scale = 0.58946
        elif self.gamma == 1.09:
            self.unscalred_area = 3.96917
            self.scale = 0.58405
        elif self.gamma == 1.1:
            self.unscalred_area = 3.96889
            self.scale = 0.57875
        elif self.gamma == 1.11:
            self.unscalred_area = 3.9686
            self.scale = 0.57353
        elif self.gamma == 1.12:
            self.unscalred_area = 3.96832
            self.scale = 0.56841
        elif self.gamma == 1.13:
            self.unscalred_area = 3.96803
            self.scale = 0.56338
        elif self.gamma == 1.14:
            self.unscalred_area = 3.96775
            self.scale = 0.55844
        elif self.gamma == 1.15:
            self.unscalred_area = 3.96747
            self.scale = 0.55358
        elif self.gamma == 1.16:
            self.unscalred_area = 3.96718
            self.scale = 0.54881
        elif self.gamma == 1.17:
            self.unscalred_area = 3.9669
            self.scale = 0.54412
        elif self.gamma == 1.18:
            self.unscalred_area = 3.96662
            self.scale = 0.53951
        elif self.gamma == 1.19:
            self.unscalred_area = 3.96633
            self.scale = 0.53497
        elif self.gamma == 1.2:
            self.unscalred_area = 3.96605
            self.scale = 0.53052
        elif self.gamma == 1.21:
            self.unscalred_area = 3.96577
            self.scale = 0.52613
        elif self.gamma == 1.22:
            self.unscalred_area = 3.96548
            self.scale = 0.52182
        elif self.gamma == 1.23:
            self.unscalred_area = 3.9652
            self.scale = 0.51758
        elif self.gamma == 1.24:
            self.unscalred_area = 3.96492
            self.scale = 0.5134
        elif self.gamma == 1.25:
            self.unscalred_area = 3.96464
            self.scale = 0.5093
        elif self.gamma == 1.26:
            self.unscalred_area = 3.96435
            self.scale = 0.50525
        elif self.gamma == 1.27:
            self.unscalred_area = 3.96407
            self.scale = 0.50128
        elif self.gamma == 1.28:
            self.unscalred_area = 3.96379
            self.scale = 0.49736
        elif self.gamma == 1.29:
            self.unscalred_area = 3.9635
            self.scale = 0.4935
        elif self.gamma == 1.3:
            self.unscalred_area = 3.96322
            self.scale = 0.48971
        elif self.gamma == 1.31:
            self.unscalred_area = 3.96294
            self.scale = 0.48597
        elif self.gamma == 1.32:
            self.unscalred_area = 3.96265
            self.scale = 0.48229
        elif self.gamma == 1.33:
            self.unscalred_area = 3.96237
            self.scale = 0.47866
        elif self.gamma == 1.34:
            self.unscalred_area = 3.96209
            self.scale = 0.47509
        elif self.gamma == 1.35:
            self.unscalred_area = 3.96181
            self.scale = 0.47157
        elif self.gamma == 1.36:
            self.unscalred_area = 3.96152
            self.scale = 0.4681
        elif self.gamma == 1.37:
            self.unscalred_area = 3.96124
            self.scale = 0.46469
        elif self.gamma == 1.38:
            self.unscalred_area = 3.96096
            self.scale = 0.46132
        elif self.gamma == 1.39:
            self.unscalred_area = 3.96067
            self.scale = 0.458
        elif self.gamma == 1.4:
            self.unscalred_area = 3.96039
            self.scale = 0.45473
        elif self.gamma == 1.41:
            self.unscalred_area = 3.96011
            self.scale = 0.4515
        elif self.gamma == 1.42:
            self.unscalred_area = 3.95983
            self.scale = 0.44832
        elif self.gamma == 1.43:
            self.unscalred_area = 3.95954
            self.scale = 0.44519
        elif self.gamma == 1.44:
            self.unscalred_area = 3.95926
            self.scale = 0.4421
        elif self.gamma == 1.45:
            self.unscalred_area = 3.95898
            self.scale = 0.43905
        elif self.gamma == 1.46:
            self.unscalred_area = 3.95869
            self.scale = 0.43604
        elif self.gamma == 1.47:
            self.unscalred_area = 3.95841
            self.scale = 0.43307
        elif self.gamma == 1.48:
            self.unscalred_area = 3.95813
            self.scale = 0.43015
        elif self.gamma == 1.49:
            self.unscalred_area = 3.95785
            self.scale = 0.42726
        elif self.gamma == 1.5:
            self.unscalred_area = 3.95756
            self.scale = 0.42441
        elif self.gamma == 1.51:
            self.unscalred_area = 3.95728
            self.scale = 0.4216
        elif self.gamma == 1.52:
            self.unscalred_area = 3.957
            self.scale = 0.41883
        elif self.gamma == 1.53:
            self.unscalred_area = 3.95671
            self.scale = 0.41609
        elif self.gamma == 1.54:
            self.unscalred_area = 3.95643
            self.scale = 0.41339
        elif self.gamma == 1.55:
            self.unscalred_area = 3.95615
            self.scale = 0.41072
        elif self.gamma == 1.56:
            self.unscalred_area = 3.95587
            self.scale = 0.40809
        elif self.gamma == 1.57:
            self.unscalred_area = 3.95558
            self.scale = 0.40549
        elif self.gamma == 1.58:
            self.unscalred_area = 3.9553
            self.scale = 0.40292
        elif self.gamma == 1.59:
            self.unscalred_area = 3.95502
            self.scale = 0.40039
        elif self.gamma == 1.6:
            self.unscalred_area = 3.95473
            self.scale = 0.39789
        elif self.gamma == 1.61:
            self.unscalred_area = 3.95445
            self.scale = 0.39542
        elif self.gamma == 1.62:
            self.unscalred_area = 3.95417
            self.scale = 0.39298
        elif self.gamma == 1.63:
            self.unscalred_ara = 3.95389
            self.scale = 0.39056
        elif self.gamma == 1.64:
            self.unscalred_area = 3.9536
            self.scale = 0.38818
        elif self.gamma == 1.65:
            self.unscalred_area = 3.95332
            self.scale = 0.38583
        elif self.gamma == 1.66:
            self.unscalred_area = 3.95304
            self.scale = 0.38351
        elif self.gamma == 1.67:
            self.unscalred_area = 3.95275
            self.scale = 0.38121
        elif self.gamma == 1.68:
            self.unscalred_area = 3.95247
            self.scale = 0.37894
        elif self.gamma == 1.69:
            self.unscalred_area = 3.95219
            self.scale = 0.3767
        elif self.gamma == 1.7:
            self.unscalred_area = 3.95191
            self.scale = 0.37448
        elif self.gamma == 1.71:
            self.unscalred_area = 3.95162
            self.scale = 0.37229
        elif self.gamma == 1.72:
            self.unscalred_area = 3.95134
            self.scale = 0.37013
        elif self.gamma == 1.73:
            self.unscalred_area = 3.95106
            self.scale = 0.36799
        elif self.gamma == 1.74:
            self.unscalred_area = 3.95077
            self.scale = 0.36587
        elif self.gamma == 1.75:
            self.unscalred_area = 3.95049
            self.scale = 0.36378
        elif self.gamma == 1.76:
            self.unscalred_area = 3.95021
            self.scale = 0.36172
        elif self.gamma == 1.77:
            self.unscalred_area = 3.94993
            self.scale = 0.35967
        elif self.gamma == 1.78:
            self.unscalred_area = 3.94964
            self.scale = 0.35765
        elif self.gamma == 1.79:
            self.unscalred_area = 3.94936
            self.scale = 0.35565
        elif self.gamma == 1.8:
            self.unscalred_area = 3.94908
            self.scale = 0.35368
        elif self.gamma == 1.81:
            self.unscalred_area = 3.94879
            self.scale = 0.35172
        elif self.gamma == 1.82:
            self.unscalred_area = 3.94851
            self.scale = 0.34979
        elif self.gamma == 1.83:
            self.unscalred_area = 3.94823
            self.scale = 0.34788
        elif self.gamma == 1.84:
            self.unscalred_area = 3.94795
            self.scale = 0.34599
        elif self.gamma == 1.85:
            self.unscalred_area = 3.94766
            self.scale = 0.34412
        elif self.gamma == 1.86:
            self.unscalred_area = 3.94738
            self.scale = 0.34227
        elif self.gamma == 1.87:
            self.unscalred_area = 3.9471
            self.scale = 0.34044
        elif self.gamma == 1.88:
            self.unscalred_area = 3.94681
            self.scale = 0.33863
        elif self.gamma == 1.89:
            self.unscalred_area = 3.94653
            self.scale = 0.33684
        elif self.gamma == 1.9:
            self.unscalred_area = 3.94625
            self.scale = 0.33506
        elif self.gamma == 1.91:
            self.unscalred_area = 3.94597
            self.scale = 0.33331
        elif self.gamma == 1.92:
            self.unscalred_area = 3.94568
            self.scale = 0.33157
        elif self.gamma == 1.93:
            self.unscalred_area = 3.9454
            self.scale = 0.32985
        elif self.gamma == 1.94:
            self.unscalred_area = 3.94512
            self.scale = 0.32815
        elif self.gamma == 1.95:
            self.unscalred_area = 3.94483
            self.scale = 0.32647
        elif self.gamma == 1.96:
            self.unscalred_area = 3.94455
            self.scale = 0.32481
        elif self.gamma == 1.97:
            self.unscalred_area = 3.94427
            self.scale = 0.32316
        elif self.gamma == 1.98:
            self.unscalred_area = 3.94399
            self.scale = 0.32153
        elif self.gamma == 1.99:
            self.unscalred_area = 3.9437
            self.scale = 0.31991
        elif self.gamma == 2.0:
            self.unscalred_area = 3.94342
            self.scale = 0.31831
        elif self.gamma == 2.01:
            self.unscalred_area = 3.94314
            self.scale = 0.31673
        elif self.gamma == 2.02:
            self.unscalred_area = 3.94285
            self.scale = 0.31516
        elif self.gamma == 2.03:
            self.unscalred_area = 3.94257
            self.scale = 0.31361
        elif self.gamma == 2.04:
            self.unscalred_area = 3.94229
            self.scale = 0.31207
        elif self.gamma == 2.05:
            self.unscalred_area = 3.94201
            self.scale = 0.31055
        elif self.gamma == 2.06:
            self.unscalred_area = 3.94172
            self.scale = 0.30904
        elif self.gamma == 2.07:
            self.unscalred_area = 3.94144
            self.scale = 0.30755
        elif self.gamma == 2.08:
            self.unscalred_area = 3.94116
            self.scale = 0.30607
        elif self.gamma == 2.09:
            self.unscalred_area = 3.94088
            self.scale = 0.3046
        elif self.gamma == 2.1:
            self.unscalred_area = 3.94059
            self.scale = 0.30315
        elif self.gamma == 2.11:
            self.unscalred_area = 3.94031
            self.scale = 0.30172
        elif self.gamma == 2.12:
            self.unscalred_area = 3.94003
            self.scale = 0.30029
        elif self.gamma == 2.13:
            self.unscalred_area = 3.93974
            self.scale = 0.29888
        elif self.gamma == 2.14:
            self.unscalred_area = 3.93946
            self.scale = 0.29749
        elif self.gamma == 2.15:
            self.unscalred_area = 3.93918
            self.scale = 0.2961
        elif self.gamma == 2.16:
            self.unscalred_area = 3.9389
            self.scale = 0.29473
        elif self.gamma == 2.17:
            self.unscalred_area = 3.93861
            self.scale = 0.29337
        elif self.gamma == 2.18:
            self.unscalred_area = 3.93833
            self.scale = 0.29203
        elif self.gamma == 2.19:
            self.unscalred_area = 3.93805
            self.scale = 0.29069
        elif self.gamma == 2.2:
            self.unscalred_area = 3.93776
            self.scale = 0.28937
        elif self.gamma == 2.21:
            self.unscalred_area = 3.93748
            self.scale = 0.28806
        elif self.gamma == 2.22:
            self.unscalred_area = 3.9372
            self.scale = 0.28677
        elif self.gamma == 2.23:
            self.unscalred_area = 3.93692
            self.scale = 0.28548
        elif self.gamma == 2.24:
            self.unscalred_area = 3.93663
            self.scale = 0.28421
        elif self.gamma == 2.25:
            self.unscalred_area = 3.93635
            self.scale = 0.28294
        elif self.gamma == 2.26:
            self.unscalred_area = 3.93607
            self.scale = 0.28169
        elif self.gamma == 2.27:
            self.unscalred_area = 3.93579
            self.scale = 0.28045
        elif self.gamma == 2.28:
            self.unscalred_area = 3.9355
            self.scale = 0.27922
        elif self.gamma == 2.29:
            self.unscalred_area = 3.93522
            self.scale = 0.278
        elif self.gamma == 2.3:
            self.unscalred_area = 3.93494
            self.scale = 0.27679
        elif self.gamma == 2.31:
            self.unscalred_area = 3.93465
            self.scale = 0.27559
        elif self.gamma == 2.32:
            self.unscalred_area = 3.93437
            self.scale = 0.27441
        elif self.gamma == 2.33:
            self.unscalred_area = 3.93409
            self.scale = 0.27323
        elif self.gamma == 2.34:
            self.unscalred_area = 3.93381
            self.scale = 0.27206
        elif self.gamma == 2.35:
            self.unscalred_area = 3.93352
            self.scale = 0.2709
        elif self.gamma == 2.36:
            self.unscalred_area = 3.93324
            self.scale = 0.26975
        elif self.gamma == 2.37:
            self.unscalred_area = 3.93296
            self.scale = 0.26862
        elif self.gamma == 2.38:
            self.unscalred_area = 3.93268
            self.scale = 0.26749
        elif self.gamma == 2.39:
            self.unscalred_area = 3.93239
            self.scale = 0.26637
        elif self.gamma == 2.4:
            self.unscalred_area = 3.93211
            self.scale = 0.26526
        elif self.gamma == 2.41:
            self.unscalred_area = 3.93183
            self.scale = 0.26416
        elif self.gamma == 2.42:
            self.unscalred_area = 3.93154
            self.scale = 0.26307
        elif self.gamma == 2.43:
            self.unscalred_area = 3.93126
            self.scale = 0.26198
        elif self.gamma == 2.44:
            self.unscalred_area = 3.93098
            self.scale = 0.26091
        elif self.gamma == 2.45:
            self.unscalred_area = 3.9307
            self.scale = 0.25984
        elif self.gamma == 2.46:
            self.unscalred_area = 3.93041
            self.scale = 0.25879
        elif self.gamma == 2.47:
            self.unscalred_area = 3.93013
            self.scale = 0.25774
        elif self.gamma == 2.48:
            self.unscalred_area = 3.92985
            self.scale = 0.2567
        elif self.gamma == 2.49:
            self.unscalred_area = 3.92957
            self.scale = 0.25567
        elif self.gamma == 2.5:
            self.unscalred_area = 3.92928
            self.scale = 0.25465
        elif self.gamma == 2.51:
            self.unscalred_area = 3.929
            self.scale = 0.25363
        elif self.gamma == 2.52:
            self.unscalred_area = 3.92872
            self.scale = 0.25263
        elif self.gamma == 2.53:
            self.unscalred_area = 3.92843
            self.scale = 0.25163
        elif self.gamma == 2.54:
            self.unscalred_area = 3.92815
            self.scale = 0.25064
        elif self.gamma == 2.55:
            self.unscalred_area = 3.92787
            self.scale = 0.24965
        elif self.gamma == 2.56:
            self.unscalred_area = 3.92759
            self.scale = 0.24868
        elif self.gamma == 2.57:
            self.unscalred_area = 3.9273
            self.scale = 0.24771
        elif self.gamma == 2.58:
            self.unscalred_area = 3.92702
            self.scale = 0.24675
        elif self.gamma == 2.59:
            self.unscalred_area = 3.92674
            self.scale = 0.2458
        elif self.gamma == 2.6:
            self.unscalred_area = 3.92646
            self.scale = 0.24485
        elif self.gamma == 2.61:
            self.unscalred_area = 3.92617
            self.scale = 0.24392
        elif self.gamma == 2.62:
            self.unscalred_area = 3.92589
            self.scale = 0.24298
        elif self.gamma == 2.63:
            self.unscalred_ara = 3.92561
            self.scale = 0.24206
        elif self.gamma == 2.64:
            self.unscalred_area = 3.92532
            self.scale = 0.24114
        elif self.gamma == 2.65:
            self.unscalred_area = 3.92504
            self.scale = 0.24023
        elif self.gamma == 2.66:
            self.unscalred_area = 3.92476
            self.scale = 0.23933
        elif self.gamma == 2.67:
            self.unscalred_area = 3.92448
            self.scale = 0.23843
        elif self.gamma == 2.68:
            self.unscalred_area = 3.92419
            self.scale = 0.23754
        elif self.gamma == 2.69:
            self.unscalred_area = 3.92391
            self.scale = 0.23666
        elif self.gamma == 2.7:
            self.unscalred_area = 3.92363
            self.scale = 0.23579
        elif self.gamma == 2.71:
            self.unscalred_area = 3.92335
            self.scale = 0.23492
        elif self.gamma == 2.72:
            self.unscalred_area = 3.92306
            self.scale = 0.23405
        elif self.gamma == 2.73:
            self.unscalred_area = 3.92278
            self.scale = 0.23319
        elif self.gamma == 2.74:
            self.unscalred_area = 3.9225
            self.scale = 0.23234
        elif self.gamma == 2.75:
            self.unscalred_area = 3.92221
            self.scale = 0.2315
        elif self.gamma == 2.76:
            self.unscalred_area = 3.92193
            self.scale = 0.23066
        elif self.gamma == 2.77:
            self.unscalred_area = 3.92165
            self.scale = 0.22983
        elif self.gamma == 2.78:
            self.unscalred_area = 3.92137
            self.scale = 0.229
        elif self.gamma == 2.79:
            self.unscalred_area = 3.92108
            self.scale = 0.22818
        elif self.gamma == 2.8:
            self.unscalred_area = 3.9208
            self.scale = 0.22736
        elif self.gamma == 2.81:
            self.unscalred_area = 3.92052
            self.scale = 0.22656
        elif self.gamma == 2.82:
            self.unscalred_area = 3.92024
            self.scale = 0.22575
        elif self.gamma == 2.83:
            self.unscalred_area = 3.91995
            self.scale = 0.22495
        elif self.gamma == 2.84:
            self.unscalred_area = 3.91967
            self.scale = 0.22416
        elif self.gamma == 2.85:
            self.unscalred_area = 3.91939
            self.scale = 0.22338
        elif self.gamma == 2.86:
            self.unscalred_area = 3.91911
            self.scale = 0.22259
        elif self.gamma == 2.87:
            self.unscalred_area = 3.91882
            self.scale = 0.22182
        elif self.gamma == 2.88:
            self.unscalred_area = 3.91854
            self.scale = 0.22105
        elif self.gamma == 2.89:
            self.unscalred_area = 3.91826
            self.scale = 0.22028
        elif self.gamma == 2.9:
            self.unscalred_area = 3.91797
            self.scale = 0.21952
        elif self.gamma == 2.91:
            self.unscalred_area = 3.91769
            self.scale = 0.21877
        elif self.gamma == 2.92:
            self.unscalred_area = 3.91741
            self.scale = 0.21802
        elif self.gamma == 2.93:
            self.unscalred_area = 3.91713
            self.scale = 0.21728
        elif self.gamma == 2.94:
            self.unscalred_area = 3.91684
            self.scale = 0.21654
        elif self.gamma == 2.95:
            self.unscalred_area = 3.91656
            self.scale = 0.2158
        elif self.gamma == 2.96:
            self.unscalred_area = 3.91628
            self.scale = 0.21507
        elif self.gamma == 2.97:
            self.unscalred_area = 3.916
            self.scale = 0.21435
        elif self.gamma == 2.98:
            self.unscalred_area = 3.91571
            self.scale = 0.21363
        elif self.gamma == 2.99:
            self.unscalred_area = 3.91543
            self.scale = 0.21292
        elif self.gamma == 3.0:
            self.unscalred_area = 3.91515
            self.scale = 0.21221
        elif self.gamma == 3.01:
            self.unscalred_area = 3.91487
            self.scale = 0.2115
        elif self.gamma == 3.02:
            self.unscalred_area = 3.91458
            self.scale = 0.2108
        elif self.gamma == 3.03:
            self.unscalred_area = 3.9143
            self.scale = 0.21011
        elif self.gamma == 3.04:
            self.unscalred_area = 3.91402
            self.scale = 0.20941
        elif self.gamma == 3.05:
            self.unscalred_area = 3.91374
            self.scale = 0.20873
        elif self.gamma == 3.06:
            self.unscalred_area = 3.91345
            self.scale = 0.20805
        elif self.gamma == 3.07:
            self.unscalred_area = 3.91317
            self.scale = 0.20737
        elif self.gamma == 3.08:
            self.unscalred_area = 3.91289
            self.scale = 0.20669
        elif self.gamma == 3.09:
            self.unscalred_area = 3.9126
            self.scale = 0.20603
        elif self.gamma == 3.1:
            self.unscalred_area = 3.91232
            self.scale = 0.20536
        elif self.gamma == 3.11:
            self.unscalred_area = 3.91204
            self.scale = 0.2047
        elif self.gamma == 3.12:
            self.unscalred_area = 3.91176
            self.scale = 0.20404
        elif self.gamma == 3.13:
            self.unscalred_area = 3.91147
            self.scale = 0.20339
        elif self.gamma == 3.14:
            self.unscalred_area = 3.91119
            self.scale = 0.20275
        elif self.gamma == 3.15:
            self.unscalred_area = 3.91091
            self.scale = 0.2021
        elif self.gamma == 3.16:
            self.unscalred_area = 3.91063
            self.scale = 0.20146
        elif self.gamma == 3.17:
            self.unscalred_area = 3.91034
            self.scale = 0.20083
        elif self.gamma == 3.18:
            self.unscalred_area = 3.91006
            self.scale = 0.20019
        elif self.gamma == 3.19:
            self.unscalred_area = 3.90978
            self.scale = 0.19957
        elif self.gamma == 3.2:
            self.unscalred_area = 3.9095
            self.scale = 0.19894
        elif self.gamma == 3.21:
            self.unscalred_area = 3.90921
            self.scale = 0.19832
        elif self.gamma == 3.22:
            self.unscalred_area = 3.90893
            self.scale = 0.19771
        elif self.gamma == 3.23:
            self.unscalred_area = 3.90865
            self.scale = 0.1971
        elif self.gamma == 3.24:
            self.unscalred_area = 3.90837
            self.scale = 0.19649
        elif self.gamma == 3.25:
            self.unscalred_area = 3.90808
            self.scale = 0.19588
        elif self.gamma == 3.26:
            self.unscalred_area = 3.9078
            self.scale = 0.19528
        elif self.gamma == 3.27:
            self.unscalred_area = 3.90752
            self.scale = 0.19468
        elif self.gamma == 3.28:
            self.unscalred_area = 3.90724
            self.scale = 0.19409
        elif self.gamma == 3.29:
            self.unscalred_area = 3.90695
            self.scale = 0.1935
        elif self.gamma == 3.3:
            self.unscalred_area = 3.90667
            self.scale = 0.19292
        elif self.gamma == 3.31:
            self.unscalred_area = 3.90639
            self.scale = 0.19233
        elif self.gamma == 3.32:
            self.unscalred_area = 3.90611
            self.scale = 0.19175
        elif self.gamma == 3.33:
            self.unscalred_area = 3.90582
            self.scale = 0.19118
        elif self.gamma == 3.34:
            self.unscalred_area = 3.90554
            self.scale = 0.1906
        elif self.gamma == 3.35:
            self.unscalred_area = 3.90526
            self.scale = 0.19004
        elif self.gamma == 3.36:
            self.unscalred_area = 3.90498
            self.scale = 0.18947
        elif self.gamma == 3.37:
            self.unscalred_area = 3.90469
            self.scale = 0.18891
        elif self.gamma == 3.38:
            self.unscalred_area = 3.90441
            self.scale = 0.18835
        elif self.gamma == 3.39:
            self.unscalred_area = 3.90413
            self.scale = 0.18779
        elif self.gamma == 3.4:
            self.unscalred_area = 3.90384
            self.scale = 0.18724
        elif self.gamma == 3.41:
            self.unscalred_area = 3.90356
            self.scale = 0.18669
        elif self.gamma == 3.42:
            self.unscalred_area = 3.90328
            self.scale = 0.18615
        elif self.gamma == 3.43:
            self.unscalred_area = 3.903
            self.scale = 0.1856
        elif self.gamma == 3.44:
            self.unscalred_area = 3.90271
            self.scale = 0.18506
        elif self.gamma == 3.45:
            self.unscalred_area = 3.90243
            self.scale = 0.18453
        elif self.gamma == 3.46:
            self.unscalred_area = 3.90215
            self.scale = 0.18399
        elif self.gamma == 3.47:
            self.unscalred_area = 3.90187
            self.scale = 0.18346
        elif self.gamma == 3.48:
            self.unscalred_area = 3.90158
            self.scale = 0.18294
        elif self.gamma == 3.49:
            self.unscalred_area = 3.9013
            self.scale = 0.18241
        elif self.gamma == 3.5:
            self.unscalred_area = 3.90102
            self.scale = 0.18189
        elif self.gamma == 3.51:
            self.unscalred_area = 3.90074
            self.scale = 0.18137
        elif self.gamma == 3.52:
            self.unscalred_area = 3.90045
            self.scale = 0.18086
        elif self.gamma == 3.53:
            self.unscalred_area = 3.90017
            self.scale = 0.18035
        elif self.gamma == 3.54:
            self.unscalred_area = 3.89989
            self.scale = 0.17984
        elif self.gamma == 3.55:
            self.unscalred_area = 3.89961
            self.scale = 0.17933
        elif self.gamma == 3.56:
            self.unscalred_area = 3.89932
            self.scale = 0.17883
        elif self.gamma == 3.57:
            self.unscalred_area = 3.89904
            self.scale = 0.17832
        elif self.gamma == 3.58:
            self.unscalred_area = 3.89876
            self.scale = 0.17783
        elif self.gamma == 3.59:
            self.unscalred_area = 3.89848
            self.scale = 0.17733
        elif self.gamma == 3.6:
            self.unscalred_area = 3.89819
            self.scale = 0.17684
        elif self.gamma == 3.61:
            self.unscalred_area = 3.89791
            self.scale = 0.17635
        elif self.gamma == 3.62:
            self.unscalred_area = 3.89763
            self.scale = 0.17586
        elif self.gamma == 3.63:
            self.unscalred_ara = 3.89735
            self.scale = 0.17538
        elif self.gamma == 3.64:
            self.unscalred_area = 3.89706
            self.scale = 0.1749
        elif self.gamma == 3.65:
            self.unscalred_area = 3.89678
            self.scale = 0.17442
        elif self.gamma == 3.66:
            self.unscalred_area = 3.8965
            self.scale = 0.17394
        elif self.gamma == 3.67:
            self.unscalred_area = 3.89622
            self.scale = 0.17347
        elif self.gamma == 3.68:
            self.unscalred_area = 3.89593
            self.scale = 0.17299
        elif self.gamma == 3.69:
            self.unscalred_area = 3.89565
            self.scale = 0.17253
        elif self.gamma == 3.7:
            self.unscalred_area = 3.89537
            self.scale = 0.17206
        elif self.gamma == 3.71:
            self.unscalred_area = 3.89509
            self.scale = 0.1716
        elif self.gamma == 3.72:
            self.unscalred_area = 3.8948
            self.scale = 0.17113
        elif self.gamma == 3.73:
            self.unscalred_area = 3.89452
            self.scale = 0.17068
        elif self.gamma == 3.74:
            self.unscalred_area = 3.89424
            self.scale = 0.17022
        elif self.gamma == 3.75:
            self.unscalred_area = 3.89396
            self.scale = 0.16977
        elif self.gamma == 3.76:
            self.unscalred_area = 3.89368
            self.scale = 0.16931
        elif self.gamma == 3.77:
            self.unscalred_area = 3.89339
            self.scale = 0.16886
        elif self.gamma == 3.78:
            self.unscalred_area = 3.89311
            self.scale = 0.16842
        elif self.gamma == 3.79:
            self.unscalred_area = 3.89283
            self.scale = 0.16797
        elif self.gamma == 3.8:
            self.unscalred_area = 3.89255
            self.scale = 0.16753
        elif self.gamma == 3.81:
            self.unscalred_area = 3.89226
            self.scale = 0.16709
        elif self.gamma == 3.82:
            self.unscalred_area = 3.89198
            self.scale = 0.16665
        elif self.gamma == 3.83:
            self.unscalred_area = 3.8917
            self.scale = 0.16622
        elif self.gamma == 3.84:
            self.unscalred_area = 3.89142
            self.scale = 0.16579
        elif self.gamma == 3.85:
            self.unscalred_area = 3.89113
            self.scale = 0.16536
        elif self.gamma == 3.86:
            self.unscalred_area = 3.89085
            self.scale = 0.16493
        elif self.gamma == 3.87:
            self.unscalred_area = 3.89057
            self.scale = 0.1645
        elif self.gamma == 3.88:
            self.unscalred_area = 3.89029
            self.scale = 0.16408
        elif self.gamma == 3.89:
            self.unscalred_area = 3.89
            self.scale = 0.16366
        elif self.gamma == 3.9:
            self.unscalred_area = 3.88972
            self.scale = 0.16324
        elif self.gamma == 3.91:
            self.unscalred_area = 3.88944
            self.scale = 0.16282
        elif self.gamma == 3.92:
            self.unscalred_area = 3.88916
            self.scale = 0.1624
        elif self.gamma == 3.93:
            self.unscalred_area = 3.88887
            self.scale = 0.16199
        elif self.gamma == 3.94:
            self.unscalred_area = 3.88859
            self.scale = 0.16158
        elif self.gamma == 3.95:
            self.unscalred_area = 3.88831
            self.scale = 0.16117
        elif self.gamma == 3.96:
            self.unscalred_area = 3.88803
            self.scale = 0.16076
        elif self.gamma == 3.97:
            self.unscalred_area = 3.88774
            self.scale = 0.16036
        elif self.gamma == 3.98:
            self.unscalred_area = 3.88746
            self.scale = 0.15995
        elif self.gamma == 3.99:
            self.unscalred_area = 3.88718
            self.scale = 0.15955
        elif self.gamma == 4.0:
            self.unscalred_area = 3.8869
            self.scale = 0.15915
        elif self.gamma == 4.01:
            self.unscalred_area = 3.88661
            self.scale = 0.15876
        elif self.gamma == 4.02:
            self.unscalred_area = 3.88633
            self.scale = 0.15836
        elif self.gamma == 4.03:
            self.unscalred_area = 3.88605
            self.scale = 0.15797
        elif self.gamma == 4.04:
            self.unscalred_area = 3.88577
            self.scale = 0.15758
        elif self.gamma == 4.05:
            self.unscalred_area = 3.88549
            self.scale = 0.15719
        elif self.gamma == 4.06:
            self.unscalred_area = 3.8852
            self.scale = 0.1568
        elif self.gamma == 4.07:
            self.unscalred_area = 3.88492
            self.scale = 0.15642
        elif self.gamma == 4.08:
            self.unscalred_area = 3.88464
            self.scale = 0.15603
        elif self.gamma == 4.09:
            self.unscalred_area = 3.88436
            self.scale = 0.15565
        elif self.gamma == 4.1:
            self.unscalred_area = 3.88407
            self.scale = 0.15527
        elif self.gamma == 4.11:
            self.unscalred_area = 3.88379
            self.scale = 0.1549
        elif self.gamma == 4.12:
            self.unscalred_area = 3.88351
            self.scale = 0.15452
        elif self.gamma == 4.13:
            self.unscalred_area = 3.88323
            self.scale = 0.15415
        elif self.gamma == 4.14:
            self.unscalred_area = 3.88294
            self.scale = 0.15377
        elif self.gamma == 4.15:
            self.unscalred_area = 3.88266
            self.scale = 0.1534
        elif self.gamma == 4.16:
            self.unscalred_area = 3.88238
            self.scale = 0.15303
        elif self.gamma == 4.17:
            self.unscalred_area = 3.8821
            self.scale = 0.15267
        elif self.gamma == 4.18:
            self.unscalred_area = 3.88181
            self.scale = 0.1523
        elif self.gamma == 4.19:
            self.unscalred_area = 3.88153
            self.scale = 0.15194
        elif self.gamma == 4.2:
            self.unscalred_area = 3.88125
            self.scale = 0.15158
        elif self.gamma == 4.21:
            self.unscalred_area = 3.88097
            self.scale = 0.15122
        elif self.gamma == 4.22:
            self.unscalred_area = 3.88069
            self.scale = 0.15086
        elif self.gamma == 4.23:
            self.unscalred_area = 3.8804
            self.scale = 0.1505
        elif self.gamma == 4.24:
            self.unscalred_area = 3.88012
            self.scale = 0.15015
        elif self.gamma == 4.25:
            self.unscalred_area = 3.87984
            self.scale = 0.14979
        elif self.gamma == 4.26:
            self.unscalred_area = 3.87956
            self.scale = 0.14944
        elif self.gamma == 4.27:
            self.unscalred_area = 3.87927
            self.scale = 0.14909
        elif self.gamma == 4.28:
            self.unscalred_area = 3.87899
            self.scale = 0.14874
        elif self.gamma == 4.29:
            self.unscalred_area = 3.87871
            self.scale = 0.1484
        elif self.gamma == 4.3:
            self.unscalred_area = 3.87843
            self.scale = 0.14805
        elif self.gamma == 4.31:
            self.unscalred_area = 3.87814
            self.scale = 0.14771
        elif self.gamma == 4.32:
            self.unscalred_area = 3.87786
            self.scale = 0.14737
        elif self.gamma == 4.33:
            self.unscalred_area = 3.87758
            self.scale = 0.14703
        elif self.gamma == 4.34:
            self.unscalred_area = 3.8773
            self.scale = 0.14669
        elif self.gamma == 4.35:
            self.unscalred_area = 3.87702
            self.scale = 0.14635
        elif self.gamma == 4.36:
            self.unscalred_area = 3.87673
            self.scale = 0.14601
        elif self.gamma == 4.37:
            self.unscalred_area = 3.87645
            self.scale = 0.14568
        elif self.gamma == 4.38:
            self.unscalred_area = 3.87617
            self.scale = 0.14535
        elif self.gamma == 4.39:
            self.unscalred_area = 3.87589
            self.scale = 0.14502
        elif self.gamma == 4.4:
            self.unscalred_area = 3.8756
            self.scale = 0.14469
        elif self.gamma == 4.41:
            self.unscalred_area = 3.87532
            self.scale = 0.14436
        elif self.gamma == 4.42:
            self.unscalred_area = 3.87504
            self.scale = 0.14403
        elif self.gamma == 4.43:
            self.unscalred_area = 3.87476
            self.scale = 0.14371
        elif self.gamma == 4.44:
            self.unscalred_area = 3.87447
            self.scale = 0.14338
        elif self.gamma == 4.45:
            self.unscalred_area = 3.87419
            self.scale = 0.14306
        elif self.gamma == 4.46:
            self.unscalred_area = 3.87391
            self.scale = 0.14274
        elif self.gamma == 4.47:
            self.unscalred_area = 3.87363
            self.scale = 0.14242
        elif self.gamma == 4.48:
            self.unscalred_area = 3.87335
            self.scale = 0.1421
        elif self.gamma == 4.49:
            self.unscalred_area = 3.87306
            self.scale = 0.14179
        elif self.gamma == 4.5:
            self.unscalred_area = 3.87278
            self.scale = 0.14147
        elif self.gamma == 4.51:
            self.unscalred_area = 3.8725
            self.scale = 0.14116
        elif self.gamma == 4.52:
            self.unscalred_area = 3.87222
            self.scale = 0.14085
        elif self.gamma == 4.53:
            self.unscalred_area = 3.87193
            self.scale = 0.14053
        elif self.gamma == 4.54:
            self.unscalred_area = 3.87165
            self.scale = 0.14022
        elif self.gamma == 4.55:
            self.unscalred_area = 3.87137
            self.scale = 0.13992
        elif self.gamma == 4.56:
            self.unscalred_area = 3.87109
            self.scale = 0.13961
        elif self.gamma == 4.57:
            self.unscalred_area = 3.87081
            self.scale = 0.1393
        elif self.gamma == 4.58:
            self.unscalred_area = 3.87052
            self.scale = 0.139
        elif self.gamma == 4.59:
            self.unscalred_area = 3.87024
            self.scale = 0.1387
        elif self.gamma == 4.6:
            self.unscalred_area = 3.86996
            self.scale = 0.1384
        elif self.gamma == 4.61:
            self.unscalred_area = 3.86968
            self.scale = 0.1381
        elif self.gamma == 4.62:
            self.unscalred_area = 3.86939
            self.scale = 0.1378
        elif self.gamma == 4.63:
            self.unscalred_ara = 3.86911
            self.scale = 0.1375
        elif self.gamma == 4.64:
            self.unscalred_area = 3.86883
            self.scale = 0.1372
        elif self.gamma == 4.65:
            self.unscalred_area = 3.86855
            self.scale = 0.13691
        elif self.gamma == 4.66:
            self.unscalred_area = 3.86827
            self.scale = 0.13661
        elif self.gamma == 4.67:
            self.unscalred_area = 3.86798
            self.scale = 0.13632
        elif self.gamma == 4.68:
            self.unscalred_area = 3.8677
            self.scale = 0.13603
        elif self.gamma == 4.69:
            self.unscalred_area = 3.86742
            self.scale = 0.13574
        elif self.gamma == 4.7:
            self.unscalred_area = 3.86714
            self.scale = 0.13545
        elif self.gamma == 4.71:
            self.unscalred_area = 3.86686
            self.scale = 0.13516
        elif self.gamma == 4.72:
            self.unscalred_area = 3.86657
            self.scale = 0.13488
        elif self.gamma == 4.73:
            self.unscalred_area = 3.86629
            self.scale = 0.13459
        elif self.gamma == 4.74:
            self.unscalred_area = 3.86601
            self.scale = 0.13431
        elif self.gamma == 4.75:
            self.unscalred_area = 3.86573
            self.scale = 0.13403
        elif self.gamma == 4.76:
            self.unscalred_area = 3.86544
            self.scale = 0.13374
        elif self.gamma == 4.77:
            self.unscalred_area = 3.86516
            self.scale = 0.13346
        elif self.gamma == 4.78:
            self.unscalred_area = 3.86488
            self.scale = 0.13318
        elif self.gamma == 4.79:
            self.unscalred_area = 3.8646
            self.scale = 0.13291
        elif self.gamma == 4.8:
            self.unscalred_area = 3.86432
            self.scale = 0.13263
        elif self.gamma == 4.81:
            self.unscalred_area = 3.86403
            self.scale = 0.13235
        elif self.gamma == 4.82:
            self.unscalred_area = 3.86375
            self.scale = 0.13208
        elif self.gamma == 4.83:
            self.unscalred_area = 3.86347
            self.scale = 0.13181
        elif self.gamma == 4.84:
            self.unscalred_area = 3.86319
            self.scale = 0.13153
        elif self.gamma == 4.85:
            self.unscalred_area = 3.8629
            self.scale = 0.13126
        elif self.gamma == 4.86:
            self.unscalred_area = 3.86262
            self.scale = 0.13099
        elif self.gamma == 4.87:
            self.unscalred_area = 3.86234
            self.scale = 0.13072
        elif self.gamma == 4.88:
            self.unscalred_area = 3.86206
            self.scale = 0.13045
        elif self.gamma == 4.89:
            self.unscalred_area = 3.86178
            self.scale = 0.13019
        elif self.gamma == 4.9:
            self.unscalred_area = 3.86149
            self.scale = 0.12992
        elif self.gamma == 4.91:
            self.unscalred_area = 3.86121
            self.scale = 0.12966
        elif self.gamma == 4.92:
            self.unscalred_area = 3.86093
            self.scale = 0.12939
        elif self.gamma == 4.93:
            self.unscalred_area = 3.86065
            self.scale = 0.12913
        elif self.gamma == 4.94:
            self.unscalred_area = 3.86037
            self.scale = 0.12887
        elif self.gamma == 4.95:
            self.unscalred_area = 3.86008
            self.scale = 0.12861
        elif self.gamma == 4.96:
            self.unscalred_area = 3.8598
            self.scale = 0.12835
        elif self.gamma == 4.97:
            self.unscalred_area = 3.85952
            self.scale = 0.12809
        elif self.gamma == 4.98:
            self.unscalred_area = 3.85924
            self.scale = 0.12784
        elif self.gamma == 4.99:
            self.unscalred_area = 3.85896
            self.scale = 0.12758
        elif self.gamma == 5.0:
            self.unscalred_area = 3.85867
            self.scale = 0.12732
        
        
        
        
        
        
        
        
            















    def gaussArea(self):
        if self.sigma == 0.01:
            self.unscaled_area = 39.89423
            self.scale = 39.89423
        elif self.sigma == 0.02:
            self.unscaled_area = 19.94711
            self.scale = 19.94711
        elif self.sigma == 0.03:
            self.unscaled_area = 13.29808
            self.scale = 13.29808
        elif self.sigma == 0.04:
            self.unscaled_area = 9.97356
            self.scale = 9.97356
        elif self.sigma == 0.05:
            self.unscaled_area = 7.97891
            self.scale = 7.97885
        elif self.sigma == 0.06:
            self.unscaled_area = 6.6513
            self.scale = 6.64904
        elif self.sigma == 0.07:
            self.unscaled_area = 5.71854
            self.scale = 5.69918
        elif self.sigma == 0.08:
            self.unscaled_area = 5.06233
            self.scale = 4.98678
        elif self.sigma == 0.09:
            self.unscaled_area = 4.61984
            self.scale = 4.43269
        elif self.sigma == 0.1:
            self.unscaled_area = 4.34002
            self.scale = 3.98942
        elif self.sigma == 0.11:
            self.unscaled_area = 4.17516
            self.scale = 3.62675
        elif self.sigma == 0.12:
            self.unscaled_area = 4.08471
            self.scale = 3.32452
        elif self.sigma == 0.13:
            self.unscaled_area = 4.03846
            self.scale = 3.06879
        elif self.sigma == 0.14:
            self.unscaled_area = 4.0164
            self.scale = 2.84959
        elif self.sigma == 0.15:
            self.unscaled_area = 4.00656
            self.scale = 2.65962
        elif self.sigma == 0.16:
            self.unscaled_area = 4.00246
            self.scale = 2.49339
        elif self.sigma == 0.17:
            self.unscaled_area = 4.00087
            self.scale = 2.34672
        elif self.sigma == 0.18:
            self.unscaled_area = 4.00029
            self.scale = 2.21635
        elif self.sigma == 0.19:
            self.unscaled_area = 4.00009
            self.scale = 2.0997
        elif self.sigma == 0.2:
            self.unscaled_area = 4.00003
            self.scale = 1.99471
        elif self.sigma == 0.21:
            self.unscaled_area = 4.00001
            self.scale = 1.89973
        elif self.sigma == 0.22:
            self.unscaled_area = 4.0
            self.scale = 1.81337
        elif self.sigma == 0.23:
            self.unscaled_area = 4.0
            self.scale = 1.73453
        elif self.sigma == 0.24:
            self.unscaled_area = 4.0
            self.scale = 1.66226
        elif self.sigma == 0.25:
            self.unscaled_area = 4.0
            self.scale = 1.59577
        elif self.sigma == 0.26:
            self.unscaled_area = 4.0
            self.scale = 1.53439
        elif self.sigma == 0.27:
            self.unscaled_area = 4.0
            self.scale = 1.47756
        elif self.sigma == 0.28:
            self.unscaled_area = 4.0
            self.scale = 1.42479
        elif self.sigma == 0.29:
            self.unscaled_area = 4.0
            self.scale = 1.37566
        elif self.sigma == 0.3:
            self.unscaled_area = 4.0
            self.scale = 1.32981
        elif self.sigma == 0.31:
            self.unscaled_area = 4.0
            self.scale = 1.28691
        elif self.sigma == 0.32:
            self.unscaled_area = 4.0
            self.scale = 1.24669
        elif self.sigma == 0.33:
            self.unscaled_area = 4.0
            self.scale = 1.20892
        elif self.sigma == 0.34:
            self.unscaled_area = 4.0
            self.scale = 1.17336
        elif self.sigma == 0.35:
            self.unscaled_area = 4.0
            self.scale = 1.13984
        elif self.sigma == 0.36:
            self.unscaled_area = 4.0
            self.scale = 1.10817
        elif self.sigma == 0.37:
            self.unscaled_area = 4.0
            self.scale = 1.07822
        elif self.sigma == 0.38:
            self.unscaled_area = 4.0
            self.scale = 1.04985
        elif self.sigma == 0.39:
            self.unscaled_area = 4.0
            self.scale = 1.02293
        elif self.sigma == 0.4:
            self.unscaled_area = 4.0
            self.scale = 0.99736
        elif self.sigma == 0.41:
            self.unscaled_area = 4.0
            self.scale = 0.97303
        elif self.sigma == 0.42:
            self.unscaled_area = 4.0
            self.scale = 0.94986
        elif self.sigma == 0.43:
            self.unscaled_area = 4.0
            self.scale = 0.92777
        elif self.sigma == 0.44:
            self.unscaled_area = 4.0
            self.scale = 0.90669
        elif self.sigma == 0.45:
            self.unscaled_area = 4.0
            self.scale = 0.88654
        elif self.sigma == 0.46:
            self.unscaled_area = 4.0
            self.scale = 0.86727
        elif self.sigma == 0.47:
            self.unscaled_area = 4.0
            self.scale = 0.84881
        elif self.sigma == 0.48:
            self.unscaled_area = 4.0
            self.scale = 0.83113
        elif self.sigma == 0.49:
            self.unscaled_area = 4.0
            self.scale = 0.81417
        elif self.sigma == 0.5:
            self.unscaled_area = 4.0
            self.scale = 0.79788
        elif self.sigma == 51:
            self.unscaled_area = 4.0
            self.scale = 0.78224
        elif self.sigma == 0.52:
            self.unscaled_area = 4.0
            self.scale = 0.7672
        elif self.sigma == 0.53:
            self.unscaled_area = 4.0
            self.scale = 0.75272
        elif self.sigma == 0.54:
            self.unscaled_area = 4.0
            self.scale = 0.73878
        elif self.sigma == 0.55:
            self.unscaled_area = 4.0
            self.scale = 0.72535
        elif self.sigma == 0.56:
            self.unscaled_area = 4.0
            self.scale = 0.7124
        elif self.sigma == 0.57:
            self.unscaled_area = 4.0
            self.scale = 0.6999
        elif self.sigma == 0.58:
            self.unscaled_area = 4.0
            self.scale = 0.68783
        elif self.sigma == 0.59:
            self.unscaled_area = 4.0
            self.scale = 0.67617
        elif self.sigma == 0.6:
            self.unscaled_area = 4.0
            self.scale = 0.6649
        elif self.sigma == 0.61:
            self.unscaled_area = 4.0
            self.scale = 0.654
        elif self.sigma == 0.62:
            self.unscaled_area = 4.0
            self.scale = 0.64346
        elif self.sigma == 0.63:
            self.unscaled_area = 4.0
            self.scale = 0.63324
        elif self.sigma == 0.64:
            self.unscaled_area = 4.0
            self.scale = 0.62335
        elif self.sigma == 0.65:
            self.unscaled_area = 4.0
            self.scale = 0.61376
        elif self.sigma == 0.66:
            self.unscaled_area = 4.0
            self.scale = 0.60446
        elif self.sigma == 0.67:
            self.unscaled_area = 4.0
            self.scale = 0.59544
        elif self.sigma == 0.68:
            self.unscaled_area = 4.0
            self.scale = 0.58668
        elif self.sigma == 0.69:
            self.unscaled_area = 4.0
            self.scale = 0.57818
        elif self.sigma == 0.7:
            self.unscaled_area = 4.0
            self.scale = 0.56992
        elif self.sigma == 0.71:
            self.unscaled_area = 4.0
            self.scale = 0.56189
        elif self.sigma == 0.72:
            self.unscaled_area = 4.0
            self.scale = 0.55409
        elif self.sigma == 0.73:
            self.unscaled_area = 4.0
            self.scale = 0.5465
        elif self.sigma == 0.74:
            self.unscaled_area = 4.0
            self.scale = 0.53911
        elif self.sigma == 0.75:
            self.unscaled_area = 4.0
            self.scale = 0.53192
        elif self.sigma == 0.76:
            self.unscaled_area = 4.0
            self.scale = 0.52492
        elif self.sigma == 0.77:
            self.unscaled_area = 4.0
            self.scale = 0.51811
        elif self.sigma == 0.78:
            self.unscaled_area = 4.0
            self.scale = 0.51146
        elif self.sigma == 0.79:
            self.unscaled_area = 4.0
            self.scale = 0.50499
        elif self.sigma == 0.8:
            self.unscaled_area = 4.0
            self.scale = 0.49868
        elif self.sigma == 0.81:
            self.unscaled_area = 4.0
            self.scale = 0.49252
        elif self.sigma == 0.82:
            self.unscaled_area = 4.0
            self.scale = 0.48651
        elif self.sigma == 0.83:
            self.unscaled_area = 4.0
            self.scale = 0.48065
        elif self.sigma == 0.84:
            self.unscaled_area = 4.0
            self.scale = 0.47493
        elif self.sigma == 0.85:
            self.unscaled_area = 4.0
            self.scale = 0.46934
        elif self.sigma == 0.86:
            self.unscaled_area = 4.0
            self.scale = 0.46389
        elif self.sigma == 0.87:
            self.unscaled_area = 4.0
            self.scale = 0.45855
        elif self.sigma == 0.88:
            self.unscaled_area = 4.0
            self.scale = 0.45334
        elif self.sigma == 0.89:
            self.unscaled_area = 4.0
            self.scale = 0.44825
        elif self.sigma == 0.9:
            self.unscaled_area = 4.0
            self.scale = 0.44327
        elif self.sigma == 0.91:
            self.unscaled_area = 4.0
            self.scale = 0.4384
        elif self.sigma == 0.92:
            self.unscaled_area = 4.0
            self.scale = 0.43363
        elif self.sigma == 0.93:
            self.unscaled_area = 4.0
            self.scale = 0.42897
        elif self.sigma == 0.94:
            self.unscaled_area = 4.0
            self.scale = 0.42441
        elif self.sigma == 0.95:
            self.unscaled_area = 4.0
            self.scale =0.41994
        elif self.sigma == 0.96:
            self.unscaled_area = 4.0
            self.scale = 0.41556
        elif self.sigma == 0.97:
            self.unscaled_area = 4.0
            self.scale = 0.41128
        elif self.sigma == 0.98:
            self.unscaled_area = 4.0
            self.scale = 0.40708
        elif self.sigma == 0.99:
            self.unscaled_area = 4.0
            self.scale = 0.40297
        elif self.sigma == 1.0:
            self.unscaled_area = 4.0
            self.scale = 0.39894
        elif self.sigma == 1.01:
            self.unscaled_area = 4.0
            self.scale = 0.39499
        elif self.sigma == 1.02:
            self.unscaled_area = 4.0
            self.scale = 0.39112
        elif self.sigma == 1.03:
            self.unscaled_area = 4.0
            self.scale = 0.38732
        elif self.sigma == 1.04:
            self.unscaled_area = 4.0
            self.scale = 0.3836
        elif self.sigma == 1.05:
            self.unscaled_area = 4.0
            self.scale = 0.37995
        elif self.sigma == 1.06:
            self.unscaled_area = 4.0
            self.scale = 0.37636
        elif self.sigma == 1.07:
            self.unscaled_area = 4.0
            self.scale = 0.37284
        elif self.sigma == 1.08:
            self.unscaled_area = 4.0
            self.scale = 0.36939
        elif self.sigma == 1.09:
            self.unscaled_area = 4.0
            self.scale = 0.366
        elif self.sigma == 1.1:
            self.unscaled_area = 4.0
            self.scale = 0.36267
        elif self.sigma == 1.11:
            self.unscaled_area = 4.0
            self.scale = 0.35941
        elif self.sigma == 1.12:
            self.unscaled_area = 4.0
            self.scale = 0.3562
        elif self.sigma == 1.13:
            self.unscaled_area = 4.0
            self.scale = 0.35305
        elif self.sigma == 1.14:
            self.unscaled_area = 4.0
            self.scale = 0.34995
        elif self.sigma == 1.15:
            self.unscaled_area = 4.0
            self.scale = 0.34691
        elif self.sigma == 1.16:
            self.unscaled_area = 4.0
            self.scale = 0.34392
        elif self.sigma == 1.17:
            self.unscaled_area = 4.0
            self.scale = 0.34098
        elif self.sigma == 1.18:
            self.unscaled_area = 4.0
            self.scale = 0.33809
        elif self.sigma == 1.19:
            self.unscaled_area = 4.0
            self.scale = 0.33525
        elif self.sigma == 1.2:
            self.unscaled_area = 4.0
            self.scale = 0.33245
        elif self.sigma == 1.21:
            self.unscaled_area = 4.0
            self.scale = 0.3297
        elif self.sigma == 1.22:
            self.unscaled_area = 4.0
            self.scale = 0.327
        elif self.sigma == 1.23:
            self.unscaled_area = 4.0
            self.scale = 0.32434
        elif self.sigma == 1.24:
            self.unscaled_area = 4.0
            self.scale = 0.32173
        elif self.sigma == 1.25:
            self.unscaled_area = 4.0
            self.scale = 0.31915
        elif self.sigma == 1.26:
            self.unscaled_area = 4.0
            self.scale = 0.31662
        elif self.sigma == 1.27:
            self.unscaled_area = 4.0
            self.scale = 0.31413
        elif self.sigma == 1.28:
            self.unscaled_area = 4.0
            self.scale = 0.31167
        elif self.sigma == 1.29:
            self.unscaled_area = 4.0
            self.scale = 0.30926
        elif self.sigma == 1.3:
            self.unscaled_area = 4.0
            self.scale = 0.30688
        elif self.sigma == 1.31:
            self.unscaled_area = 4.0
            self.scale = 0.30454
        elif self.sigma == 1.32:
            self.unscaled_area = 4.0
            self.scale = 0.30223
        elif self.sigma == 1.33:
            self.unscaled_area = 4.0
            self.scale = 0.29996
        elif self.sigma == 1.34:
            self.unscaled_area = 4.0
            self.scale = 0.29772
        elif self.sigma == 1.35:
            self.unscaled_area = 4.0
            self.scale = 0.29551
        elif self.sigma == 1.36:
            self.unscaled_area = 4.0
            self.scale = 0.29334
        elif self.sigma == 1.37:
            self.unscaled_area = 4.0
            self.scale = 0.2912
        elif self.sigma == 1.38:
            self.unscaled_area = 4.0
            self.scale = 0.28909
        elif self.sigma == 1.39:
            self.unscaled_area = 4.0
            self.scale = 0.28701
        elif self.sigma == 1.4:
            self.unscaled_area = 4.0
            self.scale = 0.28496
        elif self.sigma == 1.41:
            self.unscaled_area = 4.0
            self.scale = 0.28294
        elif self.sigma == 1.42:
            self.unscaled_area = 4.0
            self.scale = 0.28095
        elif self.sigma == 1.43:
            self.unscaled_area = 4.0
            self.scale = 0.27898
        elif self.sigma == 1.44:
            self.unscaled_area = 4.0
            self.scale = 0.27704
        elif self.sigma == 1.45:
            self.unscaled_area = 4.0
            self.scale = 0.27513
        elif self.sigma == 1.46:
            self.unscaled_area = 4.0
            self.scale = 0.27325
        elif self.sigma == 1.47:
            self.unscaled_area = 4.0
            self.scale = 0.27139
        elif self.sigma == 1.48:
            self.unscaled_area = 4.0
            self.scale = 0.26956
        elif self.sigma == 1.49:
            self.unscaled_area = 4.0
            self.scale = 0.26775
        elif self.sigma == 1.5:
            self.unscaled_area = 4.0
            self.scale = 0.26596
        elif self.sigma == 1.51:
            self.unscaled_area = 4.0
            self.scale = 0.2642
        elif self.sigma == 1.52:
            self.unscaled_area = 4.0
            self.scale = 0.26246
        elif self.sigma == 1.53:
            self.unscaled_area = 4.0
            self.scale = 0.26075
        elif self.sigma == 1.54:
            self.unscaled_area = 4.0
            self.scale = 0.25905
        elif self.sigma == 1.55:
            self.unscaled_area = 4.0
            self.scale = 0.25738
        elif self.sigma == 1.56:
            self.unscaled_area = 4.0
            self.scale = 0.25573
        elif self.sigma == 1.57:
            self.unscaled_area = 4.0
            self.scale =0.2541
        elif self.sigma == 1.58:
            self.unscaled_area = 4.0
            self.scale = 0.2525
        elif self.sigma == 1.59:
            self.unscaled_area = 4.0
            self.scale = 0.25091
        elif self.sigma == 1.6:
            self.unscaled_area = 4.0
            self.scale = 0.24934
        elif self.sigma == 1.61:
            self.unscaled_area = 4.0
            self.scale = 0.24779
        elif self.sigma == 1.62:
            self.unscaled_area = 4.0
            self.scale = 0.24626
        elif self.sigma == 1.63:
            self.unscaled_area = 4.0
            self.scale = 0.24475
        elif self.sigma == 1.64:
            self.unscaled_area = 4.0
            self.scale = 0.24326
        elif self.sigma == 1.65:
            self.unscaled_area = 4.0
            self.scale = 0.24178
        elif self.sigma == 1.66:
            self.unscaled_area = 4.0
            self.scale = 0.24033
        elif self.sigma == 1.67:
            self.unscaled_area = 4.0
            self.scale = 0.23889
        elif self.sigma == 1.68:
            self.unscaled_area = 4.0
            self.scale = 0.23747
        elif self.sigma == 1.69:
            self.unscaled_area = 4.0
            self.scale = 0.23606
        elif self.sigma == 1.7:
            self.unscaled_area = 4.0
            self.scale = 0.23467
        elif self.sigma == 1.71:
            self.unscaled_area = 4.0
            self.scale = 0.2333
        elif self.sigma == 1.72:
            self.unscaled_area = 4.0
            self.scale = 0.23194
        elif self.sigma == 1.73:
            self.unscaled_area = 4.0
            self.scale = 0.2306
        elif self.sigma == 1.74:
            self.unscaled_area = 4.0
            self.scale = 0.22928
        elif self.sigma == 1.75:
            self.unscaled_area = 4.0
            self.scale = 0.22797
        elif self.sigma == 1.76:
            self.unscaled_area = 4.0
            self.scale = 0.22667
        elif self.sigma == 1.77:
            self.unscaled_area = 4.0
            self.scale = 0.22539
        elif self.sigma == 1.78:
            self.unscaled_area = 4.0
            self.scale = 0.22412
        elif self.sigma == 1.79:
            self.unscaled_area = 4.0
            self.scale = 0.22287
        elif self.sigma == 1.8:
            self.unscaled_area = 4.0
            self.scale = 0.22163
        elif self.sigma == 1.81:
            self.unscaled_area = 4.0
            self.scale = 0.22041
        elif self.sigma == 1.82:
            self.unscaled_area = 4.0
            self.scale = 0.2192
        elif self.sigma == 1.83:
            self.unscaled_area = 4.0
            self.scale = 0.218
        elif self.sigma == 1.84:
            self.unscaled_area = 4.0
            self.scale = 0.21682
        elif self.sigma == 1.85:
            self.unscaled_area = 4.0
            self.scale = 0.21564
        elif self.sigma == 1.86:
            self.unscaled_area = 4.0
            self.scale = 0.21449
        elif self.sigma == 1.87:
            self.unscaled_area = 4.0
            self.scale = 0.21334
        elif self.sigma == 1.88:
            self.unscaled_area = 4.0
            self.scale = 0.2122
        elif self.sigma == 1.89:
            self.unscaled_area = 4.0
            self.scale = 0.21108
        elif self.sigma == 1.9:
            self.unscaled_area = 4.0
            self.scale = 0.20997
        elif self.sigma == 1.91:
            self.unscaled_area = 4.0
            self.scale = 0.20887
        elif self.sigma == 1.92:
            self.unscaled_area = 4.0
            self.scale = 0.20778
        elif self.sigma == 1.93:
            self.unscaled_area = 4.0
            self.scale = 0.20671
        elif self.sigma == 1.94:
            self.unscaled_area = 4.0
            self.scale = 0.20564
        elif self.sigma == 1.95:
            self.unscaled_area = 4.0
            self.scale = 0.20459
        elif self.sigma == 1.96:
            self.unscaled_area = 4.0
            self.scale = 0.20354
        elif self.sigma == 1.97:
            self.unscaled_area = 4.0
            self.scale = 0.20251
        elif self.sigma == 1.98:
            self.unscaled_area = 4.0
            self.scale = 0.20149
        elif self.sigma == 1.99:
            self.unscaled_area = 4.0
            self.scale = 0.20047
        elif self.sigma == 2.0:
            self.unscaled_area = 4.0
            self.scale = 0.19947
        elif self.sigma == 2.01:
            self.unscaled_area = 4.0
            self.scale = 0.19848
        elif self.sigma == 2.02:
            self.unscaled_area = 4.0
            self.scale = 0.1975
        elif self.sigma == 2.03:
            self.unscaled_area = 4.0
            self.scale = 0.19652
        elif self.sigma == 2.04:
            self.unscaled_area = 4.0
            self.scale = 0.19556
        elif self.sigma == 2.05:
            self.unscaled_area = 4.0
            self.scale = 0.19461
        elif self.sigma == 2.06:
            self.unscaled_area = 4.0
            self.scale = 0.19366
        elif self.sigma == 2.07:
            self.unscaled_area = 4.0
            self.scale = 0.19273
        elif self.sigma == 2.08:
            self.unscaled_area = 4.0
            self.scale = 0.1918
        elif self.sigma == 2.09:
            self.unscaled_area = 4.0
            self.scale = 0.19088
        elif self.sigma == 2.1:
            self.unscaled_area = 4.0
            self.scale = 0.18997
        elif self.sigma == 2.11:
            self.unscaled_area = 4.0
            self.scale = 0.18907
        elif self.sigma == 2.12:
            self.unscaled_area = 4.0
            self.scale = 0.18818
        elif self.sigma == 2.13:
            self.unscaled_area = 4.0
            self.scale = 0.1873
        elif self.sigma == 2.14:
            self.unscaled_area = 4.0
            self.scale = 0.18642
        elif self.sigma == 2.15:
            self.unscaled_area = 4.0
            self.scale = 0.18555
        elif self.sigma == 2.16:
            self.unscaled_area = 4.0
            self.scale = 0.1847
        elif self.sigma == 2.17:
            self.unscaled_area = 4.0
            self.scale = 0.18384
        elif self.sigma == 2.18:
            self.unscaled_area = 4.0
            self.scale = 0.183
        elif self.sigma == 2.19:
            self.unscaled_area = 4.0
            self.scale = 0.18217
        elif self.sigma == 2.2:
            self.unscaled_area = 4.0
            self.scale = 0.18134
        elif self.sigma == 2.21:
            self.unscaled_area = 4.0
            self.scale = 0.18052
        elif self.sigma == 2.22:
            self.unscaled_area = 4.0
            self.scale = 0.1797
        elif self.sigma == 2.23:
            self.unscaled_area = 4.0
            self.scale = 0.1789
        elif self.sigma == 2.24:
            self.unscaled_area = 4.0
            self.scale = 0.1781
        elif self.sigma == 2.25:
            self.unscaled_area = 4.0
            self.scale = 0.17731
        elif self.sigma == 2.26:
            self.unscaled_area = 4.0
            self.scale = 0.17652
        elif self.sigma == 2.27:
            self.unscaled_area = 4.0
            self.scale = 0.17575
        elif self.sigma == 2.28:
            self.unscaled_area = 4.0
            self.scale = 0.17497
        elif self.sigma == 2.29:
            self.unscaled_area = 4.0
            self.scale = 0.17421
        elif self.sigma == 2.3:
            self.unscaled_area = 4.0
            self.scale = 0.17345
        elif self.sigma == 2.31:
            self.unscaled_area = 4.0
            self.scale = 0.1727
        elif self.sigma == 2.32:
            self.unscaled_area = 4.0
            self.scale = 0.17196
        elif self.sigma == 2.33:
            self.unscaled_area = 4.0
            self.scale = 0.17122
        elif self.sigma == 2.34:
            self.unscaled_area = 4.0
            self.scale = 0.17049
        elif self.sigma == 2.35:
            self.unscaled_area = 4.0
            self.scale = 0.16976
        elif self.sigma == 2.36:
            self.unscaled_area = 4.0
            self.scale = 0.16904
        elif self.sigma == 2.37:
            self.unscaled_area = 4.0
            self.scale = 0.16833
        elif self.sigma == 2.38:
            self.unscaled_area = 4.0
            self.scale = 0.16762
        elif self.sigma == 2.39:
            self.unscaled_area = 4.0
            self.scale = 0.16692
        elif self.sigma == 2.4:
            self.unscaled_area = 4.0
            self.scale = 0.16623
        elif self.sigma == 2.41:
            self.unscaled_area = 4.0
            self.scale = 0.16554
        elif self.sigma == 2.42:
            self.unscaled_area = 4.0
            self.scale = 0.16485
        elif self.sigma == 2.43:
            self.unscaled_area = 4.0
            self.scale = 0.16417
        elif self.sigma == 2.44:
            self.unscaled_area = 4.0
            self.scale = 0.1635
        elif self.sigma == 2.45:
            self.unscaled_area = 4.0
            self.scale = 0.16283
        elif self.sigma == 2.46:
            self.unscaled_area = 4.0
            self.scale = 0.16217
        elif self.sigma == 2.47:
            self.unscaled_area = 4.0
            self.scale = 0.16152
        elif self.sigma == 2.48:
            self.unscaled_area = 4.0
            self.scale = 0.16086
        elif self.sigma == 2.49:
            self.unscaled_area = 4.0
            self.scale = 0.16022
        elif self.sigma == 2.5:
            self.unscaled_area = 4.0
            self.scale = 0.15958
        elif self.sigma == 2.51:
            self.unscaled_area = 4.0
            self.scale = 0.15894
        elif self.sigma == 2.52:
            self.unscaled_area = 4.0
            self.scale = 0.15831
        elif self.sigma == 2.53:
            self.unscaled_area = 4.0
            self.scale = 0.15768
        elif self.sigma == 2.54:
            self.unscaled_area = 4.0
            self.scale = 0.15706
        elif self.sigma == 2.55:
            self.unscaled_area = 4.0
            self.scale = 0.15645
        elif self.sigma == 2.56:
            self.unscaled_area = 4.0
            self.scale = 0.15584
        elif self.sigma == 2.57:
            self.unscaled_area = 4.0
            self.scale = 0.15523
        elif self.sigma == 2.58:
            self.unscaled_area = 4.0
            self.scale = 0.15463
        elif self.sigma == 2.59:
            self.unscaled_area = 4.0
            self.scale = 0.15403
        elif self.sigma == 2.6:
            self.unscaled_area = 4.0
            self.scale = 0.15344
        elif self.sigma == 2.61:
            self.unscaled_area = 4.0
            self.scale = 0.15285
        elif self.sigma == 2.62:
            self.unscaled_area = 4.0
            self.scale = 0.15227
        elif self.sigma == 2.63:
            self.unscaled_area = 4.0
            self.scale = 0.15169
        elif self.sigma == 2.64:
            self.unscaled_area = 4.0
            self.scale = 0.15111
        elif self.sigma == 2.65:
            self.unscaled_area = 4.0
            self.scale = 0.15054
        elif self.sigma == 2.66:
            self.unscaled_area = 4.0
            self.scale = 0.14998
        elif self.sigma == 2.67:
            self.unscaled_area = 4.0
            self.scale = 0.14942
        elif self.sigma == 2.68:
            self.unscaled_area = 4.0
            self.scale = 0.14886
        elif self.sigma == 2.69:
            self.unscaled_area = 4.0
            self.scale = 0.14831
        elif self.sigma == 2.7:
            self.unscaled_area = 4.0
            self.scale = 0.14776
        elif self.sigma == 2.71:
            self.unscaled_area = 4.0
            self.scale = 0.14721
        elif self.sigma == 2.72:
            self.unscaled_area = 4.0
            self.scale = 0.14667
        elif self.sigma == 2.73:
            self.unscaled_area = 4.0
            self.scale = 0.14613
        elif self.sigma == 2.74:
            self.unscaled_area = 4.0
            self.scale = 0.1456
        elif self.sigma == 2.75:
            self.unscaled_area = 4.0
            self.scale = 0.14507
        elif self.sigma == 2.76:
            self.unscaled_area = 4.0
            self.scale = 0.14454
        elif self.sigma == 2.77:
            self.unscaled_area = 4.0
            self.scale = 0.14402
        elif self.sigma == 2.78:
            self.unscaled_area = 4.0
            self.scale = 0.1435
        elif self.sigma == 2.79:
            self.unscaled_area = 4.0
            self.scale = 0.14299
        elif self.sigma == 2.8:
            self.unscaled_area = 4.0
            self.scale = 0.14248
        elif self.sigma == 2.81:
            self.unscaled_area = 4.0
            self.scale = 0.14197
        elif self.sigma == 2.82:
            self.unscaled_area = 4.0
            self.scale = 0.14147
        elif self.sigma == 2.83:
            self.unscaled_area = 4.0
            self.scale = 0.14097
        elif self.sigma == 2.84:
            self.unscaled_area = 4.0
            self.scale = 0.14047
        elif self.sigma == 2.85:
            self.unscaled_area = 4.0
            self.scale = 0.13998
        elif self.sigma == 2.86:
            self.unscaled_area = 4.0
            self.scale = 0.13949
        elif self.sigma == 2.87:
            self.unscaled_area = 4.0
            self.scale = 0.139
        elif self.sigma == 2.88:
            self.unscaled_area = 4.0
            self.scale = 0.13852
        elif self.sigma == 2.89:
            self.unscaled_area = 4.0
            self.scale = 0.13804
        elif self.sigma == 2.9:
            self.unscaled_area = 4.0
            self.scale = 0.13757
        elif self.sigma == 2.91:
            self.unscaled_area = 4.0
            self.scale = 0.13709
        elif self.sigma == 2.92:
            self.unscaled_area = 4.0
            self.scale = 0.13662
        elif self.sigma == 2.93:
            self.unscaled_area = 4.0
            self.scale = 0.13616
        elif self.sigma == 2.94:
            self.unscaled_area = 4.0
            self.scale = 0.13569
        elif self.sigma == 2.95:
            self.unscaled_area = 4.0
            self.scale = 0.13523
        elif self.sigma == 2.96:
            self.unscaled_area = 4.0
            self.scale = 0.13478
        elif self.sigma == 2.97:
            self.unscaled_area = 4.0
            self.scale = 0.13432
        elif self.sigma == 2.98:
            self.unscaled_area = 4.0
            self.scale = 0.13387
        elif self.sigma == 2.99:
            self.unscaled_area = 4.0
            self.scale = 0.13343
        elif self.sigma == 3.0:
            self.unscaled_area = 4.0
            self.scale = 0.13298
        elif self.sigma == 3.01:
            self.unscaled_area = 4.0
            self.scale = 0.13254
        elif self.sigma == 3.02:
            self.unscaled_area = 4.0
            self.scale = 0.1321
        elif self.sigma == 3.03:
            self.unscaled_area = 4.0
            self.scale = 0.13166
        elif self.sigma == 3.04:
            self.unscaled_area = 4.0
            self.scale = 0.13123
        elif self.sigma == 3.05:
            self.unscaled_area = 4.0
            self.scale = 0.1308
        elif self.sigma == 3.06:
            self.unscaled_area = 4.0
            self.scale = 0.13037
        elif self.sigma == 3.07:
            self.unscaled_area = 4.0
            self.scale = 0.12995
        elif self.sigma == 3.08:
            self.unscaled_area = 4.0
            self.scale = 0.12953
        elif self.sigma == 3.09:
            self.unscaled_area = 4.0
            self.scale = 0.12911
        elif self.sigma == 3.1:
            self.unscaled_area = 4.0
            self.scale = 0.12869
        elif self.sigma == 3.11:
            self.unscaled_area = 4.0
            self.scale = 0.12828
        elif self.sigma == 3.12:
            self.unscaled_area = 4.0
            self.scale = 0.12787
        elif self.sigma == 3.13:
            self.unscaled_area = 4.0
            self.scale = 0.12746
        elif self.sigma == 3.14:
            self.unscaled_area = 4.0
            self.scale = 0.12705
        elif self.sigma == 3.15:
            self.unscaled_area = 4.0
            self.scale = 0.12665
        elif self.sigma == 3.16:
            self.unscaled_area = 4.0
            self.scale = 0.12625
        elif self.sigma == 3.17:
            self.unscaled_area = 4.0
            self.scale = 0.12585
        elif self.sigma == 3.18:
            self.unscaled_area = 4.0
            self.scale = 0.12545
        elif self.sigma == 3.19:
            self.unscaled_area = 4.0
            self.scale = 0.12506
        elif self.sigma == 3.2:
            self.unscaled_area = 4.0
            self.scale = 0.12467
        elif self.sigma == 3.21:
            self.unscaled_area = 4.0
            self.scale = 0.12428
        elif self.sigma == 3.22:
            self.unscaled_area = 4.0
            self.scale = 0.1239
        elif self.sigma == 3.23:
            self.unscaled_area = 4.0
            self.scale = 0.12351
        elif self.sigma == 3.24:
            self.unscaled_area = 4.0
            self.scale = 0.12313
        elif self.sigma == 3.25:
            self.unscaled_area = 4.0
            self.scale = 0.12275
        elif self.sigma == 3.26:
            self.unscaled_area = 4.0
            self.scale = 0.12237
        elif self.sigma == 3.27:
            self.unscaled_area = 4.0
            self.scale = 0.122
        elif self.sigma == 3.28:
            self.unscaled_area = 4.0
            self.scale = 0.12163
        elif self.sigma == 3.29:
            self.unscaled_area = 4.0
            self.scale = 0.12126
        elif self.sigma == 3.3:
            self.unscaled_area = 4.0
            self.scale = 0.12089
        elif self.sigma == 3.31:
            self.unscaled_area = 4.0
            self.scale = 0.12053
        elif self.sigma == 3.32:
            self.unscaled_area = 4.0
            self.scale = 0.12016
        elif self.sigma == 3.33:
            self.unscaled_area = 4.0
            self.scale = 0.1198
        elif self.sigma == 3.34:
            self.unscaled_area = 4.0
            self.scale = 0.11944
        elif self.sigma == 3.35:
            self.unscaled_area = 4.0
            self.scale = 0.11909
        elif self.sigma == 3.36:
            self.unscaled_area = 4.0
            self.scale = 0.11873
        elif self.sigma == 3.37:
            self.unscaled_area = 4.0
            self.scale = 0.11838
        elif self.sigma == 3.38:
            self.unscaled_area = 4.0
            self.scale = 0.11803
        elif self.sigma == 3.39:
            self.unscaled_area = 4.0
            self.scale = 0.11768
        elif self.sigma == 3.4:
            self.unscaled_area = 4.0
            self.scale = 0.11734
        elif self.sigma == 3.41:
            self.unscaled_area = 4.0
            self.scale = 0.11699
        elif self.sigma == 3.42:
            self.unscaled_area = 4.0
            self.scale = 0.11665
        elif self.sigma == 3.43:
            self.unscaled_area = 4.0
            self.scale = 0.11631
        elif self.sigma == 3.44:
            self.unscaled_area = 4.0
            self.scale = 0.11597
        elif self.sigma == 3.45:
            self.unscaled_area = 4.0
            self.scale = 0.11564
        elif self.sigma == 3.46:
            self.unscaled_area = 4.0
            self.scale = 0.1153
        elif self.sigma == 3.47:
            self.unscaled_area = 4.0
            self.scale = 0.11497
        elif self.sigma == 3.48:
            self.unscaled_area = 4.0
            self.scale = 0.11464
        elif self.sigma == 3.49:
            self.unscaled_area = 4.0
            self.scale = 0.11431
        elif self.sigma == 3.5:
            self.unscaled_area = 4.0
            self.scale = 0.11398
        elif self.sigma == 3.51:
            self.unscaled_area = 4.0
            self.scale = 0.11366
        elif self.sigma == 3.52:
            self.unscaled_area = 4.0
            self.scale = 0.11334
        elif self.sigma == 3.53:
            self.unscaled_area = 4.0
            self.scale = 0.11301
        elif self.sigma == 3.54:
            self.unscaled_area = 4.0
            self.scale = 0.1127
        elif self.sigma == 3.55:
            self.unscaled_area = 4.0
            self.scale = 0.11238
        elif self.sigma == 3.56:
            self.unscaled_area = 4.0
            self.scale = 0.11206
        elif self.sigma == 3.57:
            self.unscaled_area = 4.0
            self.scale = 0.11175
        elif self.sigma == 3.58:
            self.unscaled_area = 4.0
            self.scale = 0.11144
        elif self.sigma == 3.59:
            self.unscaled_area = 4.0
            self.scale = 0.11113
        elif self.sigma == 3.6:
            self.unscaled_area = 4.0
            self.scale = 0.11082
        elif self.sigma == 3.61:
            self.unscaled_area = 4.0
            self.scale = 0.11051
        elif self.sigma == 3.62:
            self.unscaled_area = 4.0
            self.scale = 0.11021
        elif self.sigma == 3.63:
            self.unscaled_area = 4.0
            self.scale = 0.1099
        elif self.sigma == 3.64:
            self.unscaled_area = 4.0
            self.scale = 0.1096
        elif self.sigma == 3.65:
            self.unscaled_area = 4.0
            self.scale = 0.1093
        elif self.sigma == 3.66:
            self.unscaled_area = 4.0
            self.scale = 0.109
        elif self.sigma == 3.67:
            self.unscaled_area = 4.0
            self.scale = 0.1087
        elif self.sigma == 3.68:
            self.unscaled_area = 4.0
            self.scale = 0.10841
        elif self.sigma == 3.69:
            self.unscaled_area = 4.0
            self.scale = 0.10811
        elif self.sigma == 3.7:
            self.unscaled_area = 4.0
            self.scale = 0.10782
        elif self.sigma == 3.71:
            self.unscaled_area = 4.0
            self.scale = 0.10753
        elif self.sigma == 3.72:
            self.unscaled_area = 4.0
            self.scale = 0.10724
        elif self.sigma == 3.73:
            self.unscaled_area = 4.0
            self.scale = 0.10696
        elif self.sigma == 3.74:
            self.unscaled_area = 4.0
            self.scale = 0.10667
        elif self.sigma == 3.75:
            self.unscaled_area = 4.0
            self.scale = 0.10638
        elif self.sigma == 3.76:
            self.unscaled_area = 4.0
            self.scale = 0.1061
        elif self.sigma == 3.77:
            self.unscaled_area = 4.0
            self.scale = 0.10582
        elif self.sigma == 3.78:
            self.unscaled_area = 4.0
            self.scale = 0.10554
        elif self.sigma == 3.79:
            self.unscaled_area = 4.0
            self.scale = 0.10526
        elif self.sigma == 3.8:
            self.unscaled_area = 4.0
            self.scale = 0.10498
        elif self.sigma == 3.81:
            self.unscaled_area = 4.0
            self.scale = 0.10471
        elif self.sigma == 3.82:
            self.unscaled_area = 4.0
            self.scale = 0.10444
        elif self.sigma == 3.83:
            self.unscaled_area = 4.0
            self.scale = 0.10416
        elif self.sigma == 3.84:
            self.unscaled_area = 4.0
            self.scale = 0.10389
        elif self.sigma == 3.85:
            self.unscaled_area = 4.0
            self.scale = 0.10362
        elif self.sigma == 3.86:
            self.unscaled_area = 4.0
            self.scale = 0.10335
        elif self.sigma == 3.87:
            self.unscaled_area = 4.0
            self.scale = 0.10309
        elif self.sigma == 3.88:
            self.unscaled_area = 4.0
            self.scale = 0.10282
        elif self.sigma == 3.89:
            self.unscaled_area = 4.0
            self.scale = 0.10256
        elif self.sigma == 3.9:
            self.unscaled_area = 4.0
            self.scale = 0.10229
        elif self.sigma == 3.91:
            self.unscaled_area = 4.0
            self.scale = 0.10203
        elif self.sigma == 3.92:
            self.unscaled_area = 4.0
            self.scale = 0.10177
        elif self.sigma == 3.93:
            self.unscaled_area = 4.0
            self.scale = 0.10151
        elif self.sigma == 3.94:
            self.unscaled_area = 4.0
            self.scale = 0.10125
        elif self.sigma == 3.95:
            self.unscaled_area = 4.0
            self.scale = 0.101
        elif self.sigma == 3.96:
            self.unscaled_area = 4.0
            self.scale = 0.10074
        elif self.sigma == 3.97:
            self.unscaled_area = 4.0
            self.scale = 0.10049
        elif self.sigma == 3.98:
            self.unscaled_area = 4.0
            self.scale = 0.10024
        elif self.sigma == 3.99:
            self.unscaled_area = 4.0
            self.scale = 0.09999
        elif self.sigma == 4.0:
            self.unscaled_area = 4.0
            self.scale = 0.09974
        elif self.sigma == 4.01:
            self.unscaled_area = 4.0
            self.scale = 0.09949
        elif self.sigma == 4.02:
            self.unscaled_area = 4.0
            self.scale = 0.09924
        elif self.sigma == 4.03:
            self.unscaled_area = 4.0
            self.scale = 0.09899
        elif self.sigma == 4.04:
            self.unscaled_area = 4.0
            self.scale = 0.09875
        elif self.sigma == 4.05:
            self.unscaled_area = 4.0
            self.scale = 0.0985
        elif self.sigma == 406:
            self.unscaled_area = 4.0
            self.scale = 0.09826
        elif self.sigma == 4.07:
            self.unscaled_area = 4.0
            self.scale = 0.09802
        elif self.sigma == 4.08:
            self.unscaled_area = 4.0
            self.scale = 0.09778
        elif self.sigma == 4.09:
            self.unscaled_area = 4.0
            self.scale = 0.09754
        elif self.sigma == 4.1:
            self.unscaled_area = 4.0
            self.scale = 0.0973
        elif self.sigma == 4.11:
            self.unscaled_area = 4.0
            self.scale = 0.09707
        elif self.sigma == 4.12:
            self.unscaled_area = 4.0
            self.scale = 0.09683
        elif self.sigma == 4.13:
            self.unscaled_area = 4.0
            self.scale = 0.0966
        elif self.sigma == 4.14:
            self.unscaled_area = 4.0
            self.scale = 0.09636
        elif self.sigma == 4.15:
            self.unscaled_area = 4.0
            self.scale = 0.09613
        elif self.sigma == 4.16:
            self.unscaled_area = 4.0
            self.scale = 0.0959
        elif self.sigma == 4.17:
            self.unscaled_area = 4.0
            self.scale = 0.09567
        elif self.sigma == 4.18:
            self.unscaled_area = 4.0
            self.scale = 0.09544
        elif self.sigma == 4.19:
            self.unscaled_area = 4.0
            self.scale = 0.09521
        elif self.sigma == 4.2:
            self.unscaled_area = 4.0
            self.scale = 0.09499
        elif self.sigma == 4.21:
            self.unscaled_area = 4.0
            self.scale = 0.09476
        elif self.sigma == 4.22:
            self.unscaled_area = 4.0
            self.scale = 0.09454
        elif self.sigma == 4.23:
            self.unscaled_area = 4.0
            self.scale = 0.09431
        elif self.sigma == 4.24:
            self.unscaled_area = 4.0
            self.scale = 0.09409
        elif self.sigma == 4.25:
            self.unscaled_area = 4.0
            self.scale = 0.09387
        elif self.sigma == 4.26:
            self.unscaled_area = 4.0
            self.scale = 0.09365
        elif self.sigma == 4.27:
            self.unscaled_area = 4.0
            self.scale = 0.09343
        elif self.sigma == 4.28:
            self.unscaled_area = 4.0
            self.scale = 0.09321
        elif self.sigma == 4.29:
            self.unscaled_area = 4.0
            self.scale = 0.09299
        elif self.sigma == 4.3:
            self.unscaled_area = 4.0
            self.scale = 0.09278
        elif self.sigma == 4.31:
            self.unscaled_area = 4.0
            self.scale = 0.09256
        elif self.sigma == 4.32:
            self.unscaled_area = 4.0
            self.scale = 0.09235
        elif self.sigma == 4.33:
            self.unscaled_area = 4.0
            self.scale = 0.09213
        elif self.sigma == 4.34:
            self.unscaled_area = 4.0
            self.scale = 0.09192
        elif self.sigma == 4.35:
            self.unscaled_area = 4.0
            self.scale = 0.09171
        elif self.sigma == 4.36:
            self.unscaled_area = 4.0
            self.scale = 0.0915
        elif self.sigma == 4.37:
            self.unscaled_area = 4.0
            self.scale = 0.09129
        elif self.sigma == 4.38:
            self.unscaled_area = 4.0
            self.scale = 0.09108
        elif self.sigma == 4.39:
            self.unscaled_area = 4.0
            self.scale = 0.09088
        elif self.sigma == 4.4:
            self.unscaled_area = 4.0
            self.scale = 0.09067
        elif self.sigma == 4.41:
            self.unscaled_area = 4.0
            self.scale = 0.09046
        elif self.sigma == 4.42:
            self.unscaled_area = 4.0
            self.scale = 0.09026
        elif self.sigma == 4.43:
            self.unscaled_area = 4.0
            self.scale = 0.09005
        elif self.sigma == 4.44:
            self.unscaled_area = 4.0
            self.scale = 0.08985
        elif self.sigma == 4.45:
            self.unscaled_area = 4.0
            self.scale = 0.08965
        elif self.sigma == 4.46:
            self.unscaled_area = 4.0
            self.scale = 0.08945
        elif self.sigma == 4.47:
            self.unscaled_area = 4.0
            self.scale = 0.08925
        elif self.sigma == 4.48:
            self.unscaled_area = 4.0
            self.scale = 0.08905
        elif self.sigma == 4.49:
            self.unscaled_area = 4.0
            self.scale = 0.08885
        elif self.sigma == 4.5:
            self.unscaled_area = 4.0
            self.scale = 0.08865
        elif self.sigma == 4.51:
            self.unscaled_area = 4.0
            self.scale = 0.08846
        elif self.sigma == 4.52:
            self.unscaled_area = 4.0
            self.scale = 0.08826
        elif self.sigma == 4.53:
            self.unscaled_area = 4.0
            self.scale = 0.08807
        elif self.sigma == 4.54:
            self.unscaled_area = 4.0
            self.scale = 0.08787
        elif self.sigma == 4.55:
            self.unscaled_area = 4.0
            self.scale = 0.08768
        elif self.sigma == 4.56:
            self.unscaled_area = 4.0
            self.scale = 0.08749
        elif self.sigma == 4.57:
            self.unscaled_area = 4.0
            self.scale = 0.0873
        elif self.sigma == 4.58:
            self.unscaled_area = 4.0
            self.scale = 0.08711
        elif self.sigma == 4.59:
            self.unscaled_area = 4.0
            self.scale = 0.08692
        elif self.sigma == 4.6:
            self.unscaled_area = 4.0
            self.scale = 0.08673
        elif self.sigma == 4.61:
            self.unscaled_area = 4.0
            self.scale = 0.08654
        elif self.sigma == 4.62:
            self.unscaled_area = 4.0
            self.scale = 0.08635
        elif self.sigma == 4.63:
            self.unscaled_area = 4.0
            self.scale = 0.08616
        elif self.sigma == 4.64:
            self.unscaled_area = 4.0
            self.scale = 0.08598
        elif self.sigma == 4.65:
            self.unscaled_area = 4.0
            self.scale = 0.08579
        elif self.sigma == 4.66:
            self.unscaled_area = 4.0
            self.scale = 0.08561
        elif self.sigma == 4.67:
            self.unscaled_area = 4.0
            self.scale = 0.08543
        elif self.sigma == 4.68:
            self.unscaled_area = 4.0
            self.scale = 0.08524
        elif self.sigma == 4.69:
            self.unscaled_area = 4.0
            self.scale = 0.08506
        elif self.sigma == 4.7:
            self.unscaled_area = 4.0
            self.scale = 0.08488
        elif self.sigma == 4.71:
            self.unscaled_area = 4.0
            self.scale = 0.0847
        elif self.sigma == 4.72:
            self.unscaled_area = 4.0
            self.scale = 0.08452
        elif self.sigma == 4.73:
            self.unscaled_area = 4.0
            self.scale = 0.08434
        elif self.sigma == 4.74:
            self.unscaled_area = 4.0
            self.scale = 0.08417
        elif self.sigma == 4.75:
            self.unscaled_area = 4.0
            self.scale = 0.08399
        elif self.sigma == 4.76:
            self.unscaled_area = 4.0
            self.scale = 0.08381
        elif self.sigma == 4.77:
            self.unscaled_area = 4.0
            self.scale = 0.08364
        elif self.sigma == 4.78:
            self.unscaled_area = 4.0
            self.scale = 0.08346
        elif self.sigma == 4.79:
            self.unscaled_area = 4.0
            self.scale = 0.08329
        elif self.sigma == 4.8:
            self.unscaled_area = 4.0
            self.scale = 0.08311
        elif self.sigma == 4.81:
            self.unscaled_area = 4.0
            self.scale = 0.08294
        elif self.sigma == 4.82:
            self.unscaled_area = 4.0
            self.scale = 0.08277
        elif self.sigma == 4.83:
            self.unscaled_area = 4.0
            self.scale = 0.0826
        elif self.sigma == 4.84:
            self.unscaled_area = 4.0
            self.scale = 0.08243
        elif self.sigma == 4.85:
            self.unscaled_area = 4.0
            self.scale = 0.08226
        elif self.sigma == 4.86:
            self.unscaled_area = 4.0
            self.scale = 0.08209
        elif self.sigma == 4.87:
            self.unscaled_area = 4.0
            self.scale = 0.08192
        elif self.sigma == 4.88:
            self.unscaled_area = 4.0
            self.scale = 0.08175
        elif self.sigma == 4.89:
            self.unscaled_area = 4.0
            self.scale = 0.08158
        elif self.sigma == 4.9:
            self.unscaled_area = 4.0
            self.scale = 0.08142
        elif self.sigma == 4.91:
            self.unscaled_area = 4.0
            self.scale = 0.08125
        elif self.sigma == 4.92:
            self.unscaled_area = 4.0
            self.scale = 0.08109
        elif self.sigma == 4.93:
            self.unscaled_area = 4.0
            self.scale = 0.08092
        elif self.sigma == 4.94:
            self.unscaled_area = 4.0
            self.scale = 0.08076
        elif self.sigma == 4.95:
            self.unscaled_area = 4.0
            self.scale = 0.08059
        elif self.sigma == 4.96:
            self.unscaled_area = 4.0
            self.scale = 0.08043
        elif self.sigma == 4.97:
            self.unscaled_area = 4.0
            self.scale = 0.08027
        elif self.sigma == 4.98:
            self.unscaled_area = 4.0
            self.scale = 0.08011
        elif self.sigma == 4.99:
            self.unscaled_area = 4.0
            self.scale = 0.07995
        elif self.sigma == 5.0:
            self.unscaled_area = 4.0
            self.scale = 0.07979
















