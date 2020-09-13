# SEHNS Individual cases

This files run SEHNS to test the E2EL obtained in each of the four cases of the border problem.
Each case must be run individually and the scenario files adjusted accordinly.


* Case 1: Both UE connect through the same PoA in normal execution.
* Case 2: The UE connect through different PoA, before service migration.
* Case 3: Both UE connect through the same PoA, but the edge node server is on a different PoA.
* Case 4: The UE connect through different PoA, after service migration.


## Usage
1. Configure the scenario.json file to set the initial position of the vehicles.
2. Configure AdvantEDGE for port mapping
3. Update the scenarioReader script to read your scenario.
4. Run the SEHNS server (`s1`).
5. Run the publisher.
6. Run the receiver.



### Configuring the Individual Scenarios.

The SEHNS-server can be deployen in two network tiers:
- First network Tier: The edge servers are placed in the Points of Access (PoA) ::APs in json file::
- Second network Tier: The edge servers are placed in the first Point of Concentration layer (PoC)

To simulate an specific scenario, modify the initial position (initPosition) of the vehicles, the number of PoA (numberAPs) and the coverage area in the template provided and create the desired scenario.



```json
[

{
	"ScenarioId":"TestLayer1Case1",
		"carInfo":[
			{
				"v001":{
				"carSpeed":100,
				"initPosition":3
				}
			
			},
			{
				"v002":{
				"carSpeed":100,
				"initPosition":1
				}
			}
		],
	"APsInfo":
		{
			"numberAPs":1,
			"coverageArea":10040
				
		}			
}
]
```

Consider the following parameters to simulate each case:

* Case 1:
v001-initPosition<CoverageArea
v002-initPosition<CoverageArea
numberAPs=1
server: s1

* Case 2:
v001-initPosition<CoverageArea
v002-initPosition>CoverageArea
numberAPs=2
server: s1

* Case 3:
v001-initPosition>CoverageArea
v002-initPosition>CoverageArea
numberAPs=2
server: s1


* Case 4:
v001-pos>CoverageArea
v002-pos<CoverageArea
numberAPs=2
server: s2

### Configure AdvantEDGE for port mapping

To configure the port mapping in AdvantEDGE scenario, you must make sure the ports being used in this example are released.

** Used Ports **
- 3012x: TCP used for uplink --> The SEHNS client publishes to this port.
- 3017x: TCP used for downlink --> The SEHNS client listens to this port.
- 1515x: TCP used for uplink --> The SEHNS server listens to this port.
- 1415x: TCP used for downlink --> The SEHNS pushes trough this port.


PORT-MAPPING file provides a detailed example of the configuration required in AdvantEDGE scenario.




