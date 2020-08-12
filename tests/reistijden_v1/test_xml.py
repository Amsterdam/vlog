TEST_POST_TRAVEL_TIME = """
<?xml version="1.0" encoding="UTF-8" ?>
<amsterdamTravelTimes>
    <payloadPublication type="travelTime">
        <publicationReference id="PUB_AMS_PRED_TRAJECTORY_TT" version="1.0" />
        <publicationTime>2019-02-01T12:15:10Z</publicationTime>
        <measurementPeriod>
            <measurementStartTime>2019-02-01T12:14:00Z</measurementStartTime>
            <measurementEndTime>2019-02-01T12:15:00Z</measurementEndTime>
        </measurementPeriod>
        <siteMeasurements>
            <measurementSiteReference id="TRJ_1111" version="1.0">
                <measurementSiteName>traject_ZX1111_ZX1111</measurementSiteName>
                <measurementSiteType>trajectory</measurementSiteType>
                <length>1111</length>
                <locationContainedInItinerary>
                    <location index="1">
                        <lane specificLane="1">
                            <camera id="233f606b-b5f4-424e-ae2b-266e552ef111">
                                <coordinates latitude="52.111111" longitude="4.111111" />
                                <laneNumber>1</laneNumber>
                                <status>on</status>
                                <viewDirection>111</viewDirection>
                            </camera>
                        </lane>
                        <lane specificLane="2">
                            <camera id="233f606b-b5f4-424e-ae2b-266e552ef112">
                                <coordinates latitude="52.111111" longitude="4.111111" />
                                <laneNumber>1</laneNumber>
                                <status>on</status>
                                <viewDirection>111</viewDirection>
                            </camera>
                        </lane>
                    </location>
                    <location index="2">
                        <lane specificLane="1">
                            <camera id="b2a097b7-788a-48be-99d7-c923e6534222">
                                <coordinates latitude="52.222222" longitude="4.222222" />
                                <laneNumber>2</laneNumber>
                                <status>on</status>
                                <viewDirection>222</viewDirection>
                            </camera>
                        </lane>
                    </location>
                    <location index="3">
                        <lane specificLane="1">
                            <camera id="7abeb082-f73c-483b-aac9-b3644d636333">
                                <coordinates latitude="52.333333" longitude="4.333333" />
                                <laneNumber>3</laneNumber>
                                <status>on</status>
                                <viewDirection>333</viewDirection>
                            </camera>
                        </lane>
                    </location>
                    <location index="4">
                        <lane specificLane="1">
                            <camera id="233f606b-b5f4-424e-ae2b-266e552ef444">
                                <coordinates latitude="52.444444" longitude="4.444444" />
                                <laneNumber>1</laneNumber>
                                <status>on</status>
                                <viewDirection>444</viewDirection>
                            </camera>
                        </lane>
                    </location>
                </locationContainedInItinerary>
            </measurementSiteReference>
            <travelTimeData travelTimeType="predicted" estimationType="estimated">
                <travelTime>11</travelTime>
                <trafficSpeed>22</trafficSpeed>
            </travelTimeData>
        </siteMeasurements>
        <siteMeasurements>
            <measurementSiteReference id="TRJ_2222" version="1.0">
                <measurementSiteName>traject_ZX2222_ZX2222</measurementSiteName>
                <measurementSiteType>trajectory</measurementSiteType>
                <length>2222</length>
                <locationContainedInItinerary>
                    <location index="1">
                        <lane specificLane="1">
                            <camera id="1eedd82b-4228-44cd-8409-cbaa30661111">
                                <coordinates latitude="52.111111" longitude="4.111111" />
                                <laneNumber>1</laneNumber>
                                <status>on</status>
                                <viewDirection>111</viewDirection>
                            </camera>
                        </lane>
                    </location>
                    <location index="2">
                        <lane specificLane="2">
                            <camera id="6ad7ca3d-07f7-4da1-96a6-21be97912222">
                                <coordinates latitude="52.222222" longitude="4.222222" />
                                <laneNumber>2</laneNumber>
                                <status>on</status>
                                <viewDirection>222</viewDirection>
                            </camera>
                        </lane>
                    </location>
                </locationContainedInItinerary>
            </measurementSiteReference>
            <travelTimeData travelTimeType="predicted" estimationType="estimated">
                <travelTime>33</travelTime>
                <trafficSpeed>44</trafficSpeed>
            </travelTimeData>
        </siteMeasurements>
    </payloadPublication>
</amsterdamTravelTimes>
"""

TEST_POST_INDIVIDUAL_TRAVEL_TIME = """
<?xml version="1.0" encoding="UTF-8" ?>
<amsterdamTravelTimes>
    <payloadPublication type="travelTime">
        <publicationReference id="IndividualSectionTT_ESB" version="1.0" />
        <publicationTime>2019-01-22T13:23:40Z</publicationTime>
        <measurementPeriod>
            <measurementStartTime>2019-01-22T11:55:00Z</measurementStartTime>
            <measurementEndTime>2019-01-22T11:56:00Z</measurementEndTime>
        </measurementPeriod>
        <siteMeasurements>
            <measurementSiteReference id="11_1" version="1.0">
                <measurementSiteType>section</measurementSiteType>
                <length>111</length>
                <locationContainedInItinerary>
                    <location index="1">
                        <lane specificLane="lane1">
                            <camera id="111">
                                <coordinates latitude="52.111111" longitude="4.111111" />
                                <laneNumber>1</laneNumber>
                                <status>off</status>
                                <viewDirection>111</viewDirection>
                            </camera>
                        </lane>
                    </location>
                    <location index="2">
                        <lane specificLane="lane2">
                            <camera id="222">
                                <coordinates latitude="52.222222" longitude="4.222222" />
                                <laneNumber>2</laneNumber>
                                <status>off</status>
                                <viewDirection>222</viewDirection>
                            </camera>
                        </lane>
                    </location>
                </locationContainedInItinerary>
            </measurementSiteReference>
            <individualTravelTimeData>
                <licensePlate>ABCDEFGHIJKLMNOPQRSTUVWXYZ11111111111111</licensePlate>
                <vehicleCategory>M1</vehicleCategory>
                <startDetectionTime>2019-01-22T11:55:12Z</startDetectionTime>
                <endDetectionTime>2019-01-22T11:55:18Z</endDetectionTime>
                <travelTime>1</travelTime>
                <trafficSpeed>111</trafficSpeed>
            </individualTravelTimeData>
            <individualTravelTimeData>
                <licensePlate>ABCDEFGHIJKLMNOPQRSTUVWXYZ22222222222222</licensePlate>
                <vehicleCategory>M1</vehicleCategory>
                <startDetectionTime>2019-01-22T11:55:25Z</startDetectionTime>
                <endDetectionTime>2019-01-22T11:55:31Z</endDetectionTime>
                <travelTime>2</travelTime>
                <trafficSpeed>222</trafficSpeed>
            </individualTravelTimeData>
        </siteMeasurements>
        <siteMeasurements>
            <measurementSiteReference id="22_2" version="1.0">
                <measurementSiteType>section</measurementSiteType>
                <length>222</length>
                <locationContainedInItinerary>
                    <location index="1">
                        <lane specificLane="lane1">
                            <camera id="111">
                                <coordinates latitude="52.333333" longitude="4.333333" />
                                <laneNumber>1</laneNumber>
                                <status>off</status>
                                <viewDirection>111</viewDirection>
                            </camera>
                        </lane>
                    </location>
                    <location index="2">
                        <lane specificLane="lane2">
                            <camera id="222">
                                <coordinates latitude="52.444444" longitude="4.444444" />
                                <laneNumber>2</laneNumber>
                                <status>off</status>
                                <viewDirection>222</viewDirection>
                            </camera>
                        </lane>
                    </location>
                </locationContainedInItinerary>
            </measurementSiteReference>
            <individualTravelTimeData>
                <licensePlate>ABCDEFGHIJKLMNOPQRSTUVWXYZ33333333333333</licensePlate>
                <vehicleCategory>M1</vehicleCategory>
                <startDetectionTime>2019-01-22T11:55:09Z</startDetectionTime>
                <endDetectionTime>2019-01-22T11:55:17Z</endDetectionTime>
                <travelTime>8</travelTime>
                <trafficSpeed>230</trafficSpeed>
            </individualTravelTimeData>
            <individualTravelTimeData>
                <licensePlate>ABCDEFGHIJKLMNOPQRSTUVWXYZ44444444444444</licensePlate>
                <vehicleCategory>M1</vehicleCategory>
                <startDetectionTime>2019-01-22T11:55:16Z</startDetectionTime>
                <endDetectionTime>2019-01-22T11:55:24Z</endDetectionTime>
                <travelTime>8</travelTime>
                <trafficSpeed>230</trafficSpeed>
            </individualTravelTimeData>
            <individualTravelTimeData>
                <licensePlate>ABCDEFGHIJKLMNOPQRSTUVWXYZ55555555555555</licensePlate>
                <vehicleCategory>M1</vehicleCategory>
                <startDetectionTime>2019-01-22T11:55:18Z</startDetectionTime>
                <endDetectionTime>2019-01-22T11:55:26Z</endDetectionTime>
                <travelTime>8</travelTime>
                <trafficSpeed>230</trafficSpeed>
            </individualTravelTimeData>
        </siteMeasurements>
    </payloadPublication>
</amsterdamTravelTimes>
"""

TEST_POST_TRAFFIC_FLOW = """
<?xml version="1.0" encoding="UTF-8" ?>
<amsterdamTravelTimes>
    <payloadPublication type="trafficFlow">
        <publicationReference id="ExportIntensity_ESB" version="1.0" />
        <publicationTime>2019-01-20T06:46:35Z</publicationTime>
        <measurementPeriod>
            <measurementStartTime>2019-01-20T06:45:30Z</measurementStartTime>
            <measurementEndTime>2019-01-20T06:46:30Z</measurementEndTime>
        </measurementPeriod>
        <siteMeasurements>
            <measurementSiteReference id="11" version="1.0">
                <measurementSiteType>location</measurementSiteType>
                <location>
                    <lane specificLane="lane1">
                        <camera id="111">
                            <coordinates latitude="52.111111" longitude="4.111111" />
                            <laneNumber>1</laneNumber>
                            <status>on</status>
                            <viewDirection>111</viewDirection>
                        </camera>
                    </lane>
                </location>
            </measurementSiteReference>
            <trafficFlowData>
                <measuredFlow specificLane="lane1">
                    <vehicleFlow>6</vehicleFlow>
                    <numberOfInputValuesUsed>
                        <category count="6" type="Auto" />
                        <category count="2" type="Bedrijfsauto Licht" />
                    </numberOfInputValuesUsed>
                </measuredFlow>
            </trafficFlowData>
        </siteMeasurements>
        <siteMeasurements>
            <measurementSiteReference id="22" version="1.0">
                <measurementSiteType>location</measurementSiteType>
                <location>
                    <lane specificLane="lane1">
                        <camera id="222">
                            <coordinates latitude="52.222222" longitude="4.222222" />
                            <laneNumber>1</laneNumber>
                            <status>on</status>
                            <viewDirection>222</viewDirection>
                        </camera>
                    </lane>
                </location>
            </measurementSiteReference>
            <trafficFlowData>
                <measuredFlow specificLane="lane1">
                    <vehicleFlow>6</vehicleFlow>
                    <numberOfInputValuesUsed>
                        <category count="6" type="Auto" />
                    </numberOfInputValuesUsed>
                </measuredFlow>
            </trafficFlowData>
        </siteMeasurements>
        <siteMeasurements>
            <measurementSiteReference id="33" version="1.0">
                <measurementSiteType>location</measurementSiteType>
                <location>
                    <lane specificLane="lane1">
                        <camera id="333">
                            <coordinates latitude="52.333333" longitude="4.333333" />
                            <laneNumber>1</laneNumber>
                            <status>on</status>
                            <viewDirection>333</viewDirection>
                        </camera>
                    </lane>
                </location>
            </measurementSiteReference>
            <trafficFlowData>
                <measuredFlow specificLane="lane1">
                    <vehicleFlow>1</vehicleFlow>
                    <numberOfInputValuesUsed>
                        <category count="1" type="Auto" />
                    </numberOfInputValuesUsed>
                </measuredFlow>
                <measuredFlow specificLane="lane2">
                    <vehicleFlow>2</vehicleFlow>
                    <numberOfInputValuesUsed>
                        <category count="2" type="Auto" />
                    </numberOfInputValuesUsed>
                </measuredFlow>
            </trafficFlowData>
        </siteMeasurements>
    </payloadPublication>
</amsterdamTravelTimes>
"""
