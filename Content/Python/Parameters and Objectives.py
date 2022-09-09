import numpy                as np
import numpy.random         as npr
import matplotlib.pyplot    as plt 
import matplotlib.animation as ani
import csv

class Asset:  
    def __init__(asset, prevention_maintenance, corrective_maintenance, power_price, 
                        power_consumption,      crew_size,              supplies     ):
        
        # 1) OPERATION AND MAINTENANCE: PARAMETERS
        asset.personnelCost           = 0         # Monthly personnel cost per asset
        asset.salaryCost              = 0         # Monthly personnel payroll
        asset.initialSalaryCost       = 0         # Initial salary without allowances or promotions or inflation
        asset.inflationRate           = 0.0       # Inflation per year
        asset.wageRiseRate            = 0.0       # Wage rise per year
        asset.trainingCost            = 0         # Personnel training cost per month
        asset.assetPrice              = 0         # Asset acquisition cost. Depends on acquisition type (leased, constructed, bought)
        asset.assetLifeCycleInYears   = 0         # After that period, it may need replacement or maintenance
        asset.equipmentCost           = 0         # Cost of buying extra equipment
        asset.monthlySupplyCost       = 0         # Monthly costs of asset's supplies
        asset.monthlyEnergyCost       = 0         # Monthly energy consumption to operate an asset
        asset.maintenanceCost         = 0         # Per asset, per month
        asset.personnelTrainingTime   = 0         # Time in months for every parameter
        asset.maintenanceTime         = 0         # Time for asset being inactive due to maintenance
        asset.personnelRequiredToCrew = 0         # How many crew members are needed to operate an asset
        asset.personnelAvailability   = 0         # If and how many people are available or need training in order to operate an asset
        asset.unplannedMaintenance    = 0         # Unplanned maintenance may occur due to possible malfunction. Therefore needs to define more parameters
                                                  # a) List of possible malfunctions, b) Replacement cost, c) Probability of occurance  
        
        # 1) OPERATION AND MAINTENANCE: OBJECTIVES
        asset.minimizeOperateAndMaintenanceCost          = 0   # Minimize O&M costs of an asset
        asset.minimizeMaintenanceAndWaitingTimesInMonths = 0   # Minimize time of asset being inactive due to maintenance
        asset.maximizeAvailabilityPercentage             = 0.0 # Maximize the availability of assets in order to always have the fleet needed in case of a conflict
        
        # 2) PERFORMANCE AND EFFECTIVENESS: PARAMETERS
        asset.assetType                              = " " # If asset is a vessel, radar, combat system
        asset.assetPrice                             = 0   # Total asset price -TBD later
        asset.threatType                             = " " # Threat type, size, asset configuration

        asset.radarParameters                        = {"centralFrequencyInGHz"  :   0,
                                                        "radarPowerInKW"         :   0,
                                                        "antennaDiameterInM"     :   0,
                                                        "bandwidthInKHz"         :   0,
                                                        
                                                        "spaceCoveragePercentage": 100,
                                                        "timeCoveragePercentage" : 100,
                                                
                                                        "maxRangeInKm"           :   0,
                                                        "performancePercentage"  : 100,
                                                        "timeOfflinePercentage"  :   0, 
                                                        
                                                        "radarPrice"                    : 100000,   # Cost-related radar params
                                                        
                                                        "radarMonthlyPowerCost"         :   5000,
                                                        "radarMonthlySupplyCost"        :    500,
                                                        "radarMonthlyEquipmentCost"     :    200,
                                                        "radarOperationalCost"          :   5700,
                                                        
                                                        "radarPreventiveMaintenanceCost":    100,
                                                        "radarCorrectiveMaintenanceCost":   2000,
                                                        "radarMaintenanceCost"          :   2100
                                                        
                                                        
                                                        
                                                     } 
                                                     # Parameters for radar system. E.g. Central frequency (GHz), Radar power (kW), 
                                                     # Antenna diameter (m), Bandwidth (KHz), ADDITIONALLY after radar document, 
                                                     # 1a) % space coverage 1b) % time coverage 2b1) MaxRange, 2b2) Degradation of performance 
                                                     # as a percentage of total time 2b3) Percentage of time per year offline due to maintenance
                                                     #

        asset.missileParameters                      = {"numberOfMissiles "      : 0,
                                                        "speedInMeterPerSecond"  : 0,
                                                        "maxRangeInKm"           : 0,
                                                        "flightAltitudeInMeters" : 0
                                                     }
                                                     # Parameters for different types of Missile systems (SSM, SAM). E.g. an SSM has
                                                     # params like this: Number of missiles, Speed (m/s), Max range (Km), Flight altitude (m)

        asset.gunParameters                          = {"maxRangeInKm"                    : 0,
                                                        "projectileSpeedInMeterPerSecond" : 0,
                                                        "fireRateInProjPerMin"            : 0
                                                     }
                                                     # E.g. Max range (Km), Projectile speed (m/s), Fire rate (Proj./min)

        asset.topedoParameters                       = {"numberOfTorpedos "    : 0,
                                                        "warheadInKilos"       : 0,
                                                        "batteryLifeInMinutes" : 0,
                                                        "speedInKt"            : 0,
                                                        "maxRangeInKm"         : 0
                                                     }
                                                     # E.g. Number, Warhead (kg), Battery life (min), Speed (kt), Max range (Km)

        asset.warshipParameters                      = {"numberOfPlatform "      : 1,
                                                        "numberOfGuns"           : 0,
                                                        "numberOfRadars"         : 0,
                                                        "numberOfMissileSystems" : 0,
                                                        "numberOfTorpedoSystems" : 0
                                                     }
                                                     # Warship is a combination of assets, consist of a platform and extra guns/radars/missile systems
        
        asset.scenario                               = " " # In order to measure the performance and effectiveness of an asset, a custom scenarion is needed
                                                           # e.g. an enemy aircraft is violating area with friendly vessel. We want to know reaction time
                                                           # of friendly vessel, probability to intercept the threat etc.
                                                    
        asset.vulnerabilities                        = " " # Asset vulnerabilities in combat scenarios, depending on the threat type and configuration
        
        # 2) PERFORMANCE AND EFFECTIVENESS: OBJECTIVES
        asset.maximizePerformancePercentage          = 0.0
                                                     # Given a list of all available assets, the system will perform calculations to determine
                                                     # which combination of assets to acquire and in what quantities, in order to maximize the
                                                     # performance of a certain task.
                                                    
        asset.maximizeEffectivenessPercentage        = 0.0
                                                     # Given a conflict situation, the simulation will decide which asset configuration is the 
                                                     # most effective. The overall effectiveness is computed by adding the performance of each asset
        
        asset.calculateMeasureOfEffectiveness        = 0.0
                                                     # MOEs are probabilistic measures of the operational performance of the system, calculated from
                                                     # the measure of performance of each asset
                                                    
        asset.maximizeAreaOfCoverage                 = 0
                                                     # To maximize the area of coverage of the fleet by determining the asset configuration and positioning
                                                     
        asset.minimizeDetectionTime                  = 0.0
                                                     # Minimization of the threat's detection time. Determine, for example, which radar setup is most 
                                                     # effective against an enemy aircraft in order to detect and intercept it fast
        
        # 3) SCENARIO UNFOLDING: PARAMETERS
        asset.state                                  = "Idle"  # Scenario Unfolding module state. Can either be 'Idle', 'Maintenance', 'Conflict', 'Mission'
#       asset.assetTypeScenarioUnfolding             = " "     # ALREADY EXISTS. Vessel or radar or system etc
#       asset.assetPriceScenarioUnfolding            = 0       # ALREADY EXISTS. Asset acquistion cost. Depends on the acquisition type (Leasing, constructed, bought)
        asset.operateAndMaintainCost                 = 0       # Asset's operational and maintenance cost. Can be broken down to extra cost relating to personnel
                                                               # equipment, gas, maintenance, etc
                                                    
        asset.assetLifeCycleInYearsScenarioUnfolding = 0       # Estimated life time until asset becomes non functional. In this case it is replaced or removed. Time
                                                               # is measured in years. An estimation of that may be given from the asset manufacturers.
                                                    
        asset.modularity                             = " "     # Ability to get upgraded or improved from technological aspect. Non measurable.
        asset.availability                           = " "     # Asset is available, that means ready to use, in a specific time moment or time period during a mission.
                                                               # Battle scenario needed.
                                                    
        asset.enemyAsset                             = {"numberOfPlatform "      : 1,
                                                        "numberOfGuns"           : 0,
                                                        "numberOfRadars"         : 0,
                                                        "numberOfMissileSystems" : 0,
                                                        "numberOfTorpedoSystems" : 0
                                                     }
                                                     # Enemy equipment features. Info needed to calculate effectiveness of an asset configuration towards enemy.
                                                     
        asset.warshipConfiguration                   = {"totalNumberOfPlatforms"      : 1,
                                                        "totalNumberOfGuns"           : 0,
                                                        "totalNumberOfRadars"         : 0,
                                                        "totalNumberOfMissileSystems" : 0,
                                                        "totalNumberOfTorpedoSystems" : 0
                                                     }
                                                     # The number of warships and which 'warship parameters' include each of them. Related to warshipParameters
                                                     
        asset.fleetList                              = {" ", " ", " "}          # A list of warships
        asset.replacementCost                        = 0                        # Cost in case of asset replacement
        asset.replacementPeriod                      = {"from": " ", "to": " "} # Period of the replacement. Depending on the replacement, the asset could be inactive.
        asset.replacementFrequencyTimesPerYear       = 0                        # How often the asset needs replacement. For example, how many times per year, per month etc.
        asset.upgradeCost                            = 0                        # The cost to upgrade an asset or a part of it
        asset.upgradePeriod                          = {"from": " ", "to": " "} # The period which an asset is inactive due to being upgraded
        asset.disposalCost                           = 0                        # The cost to dispose an asset
        asset.risksAndUncertainties                  = " "                      # The risks and uncertainties of events to occur, e.g. Unplanned Maintenance or Risk of Conflict etc
        asset.probabilities                          = " "                      # The probability to change the state of an asset (Idle, Maintenance, Conflict, Mission)
        
        # 3) SCENARIO UNFOLDING: OBJECTIVES
        asset.realisticStateTransitioning            = " "              
                                                     # In order to make the vessel's state transistions as realistic as possible, the system will analyze datasets
                                                     # provided by other DECISMAR modules, taking into consideration the probability and the uncertainty of each
                                                     # transition occuring
                                                    
        asset.feedDataToOtherComponents              = " "
                                                     # The transition of the vessel's states, feeds data to the other Components of the Simulation Module and 
                                                     # and affects their functionality. For example, transitioning the vessel to the Maintenance state will activate
                                                     # the Operation and Maintenance Component, increasing the vessel's Operation and Maintenance cost, but also 
                                                     # activate the Performance and Effectiveness Component, reducing the asset's Availability

#----------------EDW SYNEXIZOYME PAIRONTAS DEDOMENA APO TO ALLO ARXEIO--------------------

        asset.prevention_maintenance = prevention_maintenance
        asset.corrective_maintenance = corrective_maintenance
        asset.power_price            = power_price
        asset.power_consumption      = power_consumption
        asset.crew_size              = crew_size
        asset.supplies               = supplies
        
    def maintenance(self,time):
        return float(self.prevention_maintenance) +0.01*(time**2)*npr.triangular(0, float(self.corrective_maintenance), float(self.corrective_maintenance)*2)

    def operational(self, time):
        power_cost      = float(self.power_price) + time*npr.triangular(0.001, 0.005, 0.007) * npr.uniform(float(self.power_consumption)-5000,float(self.power_consumption)+5000)
        supply_cost    = npr.uniform(float(self.supplies), float(self.supplies)+2000)
        equipment_cost = npr.uniform(float(self.crew_size),float(self.crew_size)+2000)
        return power_cost + supply_cost + equipment_cost
       
    def life_cycle(self,time):
        # Maintenance part
        self.prevention_maintenance_list = []
        self.corrective_maintenance_list = []
        self.           maintenance_list = []

        # Operational/Logistics part
        self.    power_cost_list = []
        self.   supply_cost_list = []
        self.equipment_cost_list = []
        self.   operational_list = []        
               
        total_maintenance = 0
        total_operational = 0
        total_costs       = 0 
        
        for i in range(1, time+1):
            #--------------------Maintenance part----------------------
            total_maintenance += self.maintenance(i)
            
            self.corrective_maintenance_list.append(total_maintenance - float(self.prevention_maintenance))
            self.prevention_maintenance_list.append(float(self.prevention_maintenance) + 5*i)  
            self.           maintenance_list.append(total_maintenance)
            
            # Operational/Logistics part
            total_operational += self.operational(i)
            
            self.    power_cost_list.append(float(self.power_price) + i*npr.triangular(0.001, 0.005, 0.007) * npr.uniform(float(self.power_consumption)-5000, float(self.power_consumption)+5000))
            self.   supply_cost_list.append(npr.uniform(float(self.supplies), float(self.supplies) +2000))  
            self.equipment_cost_list.append(npr.uniform(float(self.crew_size),float(self.crew_size)+2000))  
            self.   operational_list.append(total_operational)
            
            total_costs += self.operational(i) + self.maintenance(i)
        return total_costs
    
#---------------------------------------------------------------------------       

fig, ax = plt.subplots(1,3)    
#radar = Asset(1000, 10000, 2, 20000, 200, 10000)
#radar.life_cycle(361)

with open(r'C:\Users\stylianos\Documents\Unreal Projects\depth\Content\Python\Radar_list.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        line_count += 1
        print("\n",row["Asset Name"],             row["Monthly power cost"],          row["Monthly supply cost"], 
                   row["Monthly equipment cost"], row["Preventive maintenance cost"], row["Corrective maintenance cost"], "\n")
    print(f'Processed {line_count} lines.')

radarNameFromCSV                      = row[                 "Asset Name"]  
radarPowerCostFromCSV                 = row[         "Monthly power cost"]
radarSupplyCostFromCSV                = row[        "Monthly supply cost"]
radarEquipmentCostFromCSV             = row[     "Monthly equipment cost"]
radarPreventiveMaintenanceCostFromCSV = row["Preventive maintenance cost"]
radarCorrectiveMaintenanceCostFromCSV = row["Corrective maintenance cost"]

radar = Asset(radarPreventiveMaintenanceCostFromCSV, radarCorrectiveMaintenanceCostFromCSV, 1, radarPowerCostFromCSV, 200, radarSupplyCostFromCSV)
radar.life_cycle(361)

print("\n",radarNameFromCSV,          radarPowerCostFromCSV,                 radarSupplyCostFromCSV, 
           radarEquipmentCostFromCSV, radarPreventiveMaintenanceCostFromCSV, radarCorrectiveMaintenanceCostFromCSV, "\n")

# TITLOI EPIMEROYS, AN XREIASTOYN
ax[0].set_title(radarNameFromCSV + ' Acquisition Planning',                fontsize='16')
ax[1].set_title(radarNameFromCSV + ' Maintenance cost analysis',           fontsize='16')
ax[2].set_title(radarNameFromCSV + ' Operational/Logistics cost analysis', fontsize='16')

# Maintenance part
prevention_maintenance = radar.prevention_maintenance_list
corrective_maintenance = radar.corrective_maintenance_list
maintenance            = radar.           maintenance_list

# Operational/Logistics part
power_cost     = radar.    power_cost_list
supply_cost    = radar.   supply_cost_list
equipment_cost = radar.equipment_cost_list
operational    = radar.   operational_list

x1_data  = []
y1_data  = []
x2_data  = []
y2_data  = []
x3_data  = []
y3_data  = []
x4_data  = []
y4_data  = []
x5_data  = []
y5_data  = []
x6_data  = []
y6_data  = []
x7_data  = []
y7_data  = []
x8_data  = []
y8_data  = []
x9_data  = []
y9_data  = []
x10_data = []
y10_data = []

#--------------Diagram 1: Maintenance-----------------
line1, = ax[1].plot(0,0, '-r', label = 'Prevention maintenance cost')
line2, = ax[1].plot(0,0, '-g', label = 'Corrective maintenance cost')
line3, = ax[1].plot(0,0,'--b', label =      'Total maintenance cost')

#--------------Diagram 2: Operational/Logistics-----------------
line4, = ax[2].plot(0,0, '-r', label =                       'Power cost')
line5, = ax[2].plot(0,0, '-g', label =                      'Supply cost')
line6, = ax[2].plot(0,0, '-y', label =                   'Equipment cost')
line7, = ax[2].plot(0,0,'--b', label = 'Total operational/Logistics cost')


def animation_frame(i):
    tit = "{} years and {} months"
    tit1 = "Time: " + tit.format((int)(i/12),i%12)
    fig.suptitle(tit1, fontsize='20')
    print(i)

    #------------------------Barchart part------------------------
    names = np.array(["Maintenance cost", "Operational/Logistics cost", "Total cost"])
    ma = maintenance[i]
    op = operational[i]

    to = ma + op 
    
    percentage = np.array([ma, op, to])
    c = ['orange','red','green','blue']
    ax[0].bar(names, percentage, color=c)
    ax[0].set_ylabel('Money (euro)')
    
    #-------------------Maintenance part------------------------
    x1_data.append(i), x2_data.append(i), x3_data.append(i)
    curr_ylim = 1.05 * maintenance[i]   

    ax[1].set_xlim(0, i)  
    ax[1].set_ylim(0, curr_ylim)
    ax[1].legend(loc='upper left', frameon=False)
    ax[1].set_ylabel('Money (euro)')
    ax[1].set_xlabel('Time (months)')
    
    y1_data.append(prevention_maintenance[i]), 
    y2_data.append(corrective_maintenance[i]), 
    y3_data.append(maintenance[i])      

    line1.set_xdata(x1_data), line1.set_ydata(y1_data), 
    line2.set_xdata(x2_data), line2.set_ydata(y2_data), 
    line3.set_xdata(x3_data), line3.set_ydata(y3_data), 
       
    #return line1, line2, line3
    
    #-----------------Operational/Logistics part------------------
    x4_data.append(i), x5_data.append(i), x6_data.append(i), x7_data.append(i)
    curr_ylim = 1.05 * operational[i]   

    ax[2].set_xlim(0, i)  
    ax[2].set_ylim(0, curr_ylim)
    ax[2].legend(loc='upper left', frameon=False)
    ax[2].set_ylabel('Money (euro)')
    ax[2].set_xlabel('Time (months)')

    y4_data.append(    power_cost[i]), 
    y5_data.append(   supply_cost[i]), 
    y6_data.append(equipment_cost[i]),      
    y7_data.append(   operational[i]), 

    print(power_cost[i], supply_cost[i], equipment_cost[i], operational[i])
    line4.set_xdata(x4_data), line4.set_ydata(y4_data), 
    line5.set_xdata(x5_data), line5.set_ydata(y5_data), 
    line6.set_xdata(x6_data), line6.set_ydata(y6_data), 
    line7.set_xdata(x7_data), line7.set_ydata(y7_data), 
      
    #return line4, line5, line5, line7
    
plt.subplots_adjust(bottom = 0.2, top = 0.9)

animator = ani.FuncAnimation(fig, func=animation_frame, frames=np.arange(0,361,1), interval = 0.0001, repeat = False)
plt.show()

#print("Let's read a CSV file...")

#-----------------------TROPOS 1: ME PANDAS---------------------------
#df = pd.read_csv(r'C:\Users\dkosmad.ICS\Desktop\Radar_list.csv', encoding='unicode_escape')
#print(df)

#-----------------------TROPOS 2: CSV->DICTIONARY---------------------
#with open(r'C:\Users\dkosmad.ICS\Desktop\Radar_list.csv', mode='r') as csv_file:
#    csv_reader = csv.DictReader(csv_file)
#    line_count = 0
#    #print(csv_reader.fieldnames)
    
#    for row in csv_reader:
#        if line_count == 0:
#            #print(f'Column names are {", ".join(row)}')
#            line_count += 1
#        line_count += 1
#        print("\n",row)
#    print(f'Processed {line_count} lines.')

#print("\nLet's write to CSV file...")
#f = open(r'C:\Users\dkosmad.ICS\Desktop\Radar_list_new.csv', mode='w') 

#with f as csv_file:
#    csv_writer = csv.DictWriter(csv_file, delimiter='', quotechar='|')
#    csv_writer.writerows(([" ","3"], ["Asset name", "test2"]))
    
    
