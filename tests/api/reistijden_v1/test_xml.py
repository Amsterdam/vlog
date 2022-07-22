TEST_POST_TRAVEL_TIME = """
<?xml version="1.0" encoding="UTF-8" ?>
<amsterdamTravelTimes>
    <payloadPublication type="travelTime">
        <publicationReference id="PUB_AMS_PRED_TRAJECTORY_TT" version="1.0" />
        <publicationTime>2019-02-01T12:15:10Z</publicationTime>
        <measurementPeriod>
            <measurementStartTime>2019-02-01T12:14:00Z</measurementStartTime>
            <measurementEndTime>2019-02-01T12:15:00Z</measurementEndTime>
            <duration>10</duration>
        </measurementPeriod>
        <siteMeasurements>
            <measurementSiteReference id="TRJ_1" version="1.0">
                <measurementSiteName>traject_ZX1</measurementSiteName>
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
            <travelTimeData travelTimeType="raw">
                <travelTime>-1</travelTime>
                <trafficSpeed>-1</trafficSpeed>
            </travelTimeData>
            <travelTimeData travelTimeType="representative">
                <travelTime>-1</travelTime>
                <trafficSpeed>-1</trafficSpeed>
            </travelTimeData>
            <travelTimeData travelTimeType="processed" dataQuality="38.000000" estimationType="estimated" numberOfInputValuesUsed="10">
                <travelTime>178</travelTime>
                <trafficSpeed>34</trafficSpeed>
                <dataError>true</dataError>
            </travelTimeData>
        </siteMeasurements>
        <siteMeasurements>
            <measurementSiteReference id="TRJ_2" version="1.0">
                <measurementSiteName>traject_ZX2</measurementSiteName>
                <measurementSiteType>trajectory</measurementSiteType>
                <length>1111</length>
                <locationContainedInItinerary>
                    <location index="1">
                        <lane specificLane="1">
                            <camera id="233f606b-b5f4-424e-ae2b-266e552ef211">
                                <coordinates latitude="52.111111" longitude="4.111111" />
                                <laneNumber>1</laneNumber>
                                <status>on</status>
                                <viewDirection>111</viewDirection>
                            </camera>
                        </lane>
                    </location>
                    <location index="2">
                        <lane specificLane="1">
                            <camera id="b2a097b7-788a-48be-99d7-c923e6534212">
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
        </siteMeasurements>
    </payloadPublication>
</amsterdamTravelTimes>
"""

TEST_POST_INDIVIDUAL_TRAVEL_TIME_SINGLE_MEASUREMENT = """
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
                    <vehicleFlow>7</vehicleFlow>
                    <numberOfInputValuesUsed>
                        <category count="6" type="" />
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

TEST_POST_EMPTY = """
<?xml version="1.0" encoding="UTF-8" ?>
<amsterdamTravelTimes>
    <payloadPublication type="individualTravelTime">
        <publicationReference id="AMS_PUB_INDIVIDUAL_TT" version="1.0" />
        <publicationTime>2020-08-26T03:28:28Z</publicationTime>
        <measurementPeriod>
            <measurementStartTime>2020-08-25T02:00:00Z</measurementStartTime>
            <measurementEndTime>2020-08-25T02:01:00Z</measurementEndTime>
        </measurementPeriod>
    </payloadPublication>
</amsterdamTravelTimes>
"""

# The message below was a real message that was received
TEST_POST_WRONG_TAGS = """
<?xml version="1.0" encoding="UTF-8" ?>
    <mismatchedtag>
        <payloadPublication type="individualTravelTime">
            <publicationReference id="AMS_PUB_INDIVIDUAL_TT" version="1.0" />
            <publicationTime>2020-08-26T03:28:28Z</publicationTime>
            <measurementPeriod>
                <measurementStartTime>2020-08-25T02:00:00Z</measurementStartTime>
                <measurementEndTime>2020-08-25T02:01:00Z</measurementEndTime>
            </measurementPeriod>
        </payloadPublication>
    <>
</amsterdamTravelTimes>
"""

TEST_POST_MISSING_locationContainedInItinerary = """
<?xml version="1.0" encoding="UTF-8" ?>
<amsterdamTravelTimes>
    <payloadPublication type="travelTime">
        <publicationReference id="AMS_PUB_ALL_SECTION_TT" version="1.0" />
        <publicationTime>2021-03-18T11:33:07Z</publicationTime>
        <measurementPeriod>
            <measurementStartTime>2021-03-18T11:32:00Z</measurementStartTime>
            <measurementEndTime>2021-03-18T11:33:00Z</measurementEndTime>
        </measurementPeriod>
        <siteMeasurements>
            <measurementSiteReference id="SEC_1" version="1.0">
                <measurementSiteName>S101_V_S102_T_S100_M</measurementSiteName>
                <measurementSiteType>section</measurementSiteType>
                <length>123</length>
                <locationContainedInItinerary>
                    <location index="1">
                        <lane specificLane="-2">
                            <camera id="a8f116f1-4538-433f-9f18-c8eee204b171">
                                <coordinates latitude="52.123456" longitude="4.123456" />
                                <laneNumber>-2</laneNumber>
                                <status>on</status>
                                <viewDirection>270</viewDirection>
                            </camera>
                        </lane>
                        <lane specificLane="-1">
                            <camera id="3a6b0a00-7e93-48b9-bc06-9e0871a20d18">
                                <coordinates latitude="52.123456" longitude="4.123456" />
                                <laneNumber>-1</laneNumber>
                                <status>on</status>
                                <viewDirection>270</viewDirection>
                            </camera>
                        </lane>
                    </location>
                    <location index="2">
                        <lane specificLane="1">
                            <camera id="f97f1505-a2f6-4683-9068-5a5a950cccbc">
                                <coordinates latitude="52.123456" longitude="4.123456" />
                                <laneNumber>1</laneNumber>
                                <status>on</status>
                                <viewDirection>180</viewDirection>
                            </camera>
                        </lane>
                    </location>
                </locationContainedInItinerary>
            </measurementSiteReference>
            <travelTimeData travelTimeType="raw" numberOfInputValuesUsed="8">
                <travelTime>123</travelTime>
                <trafficSpeed>12</trafficSpeed>
                <numberOfInputValuesUsed>
                    <category count="6" type="Auto" />
                    <category count="1" type="Bedrijfsauto Licht" />
                    <category count="1" type="Bedrijfsauto Zwaar" />
                </numberOfInputValuesUsed>
            </travelTimeData>
            <travelTimeData travelTimeType="representative" numberOfInputValuesUsed="7">
                <travelTime>123</travelTime>
                <trafficSpeed>12</trafficSpeed>
                <numberOfInputValuesUsed>
                    <category count="5" type="Auto" />
                    <category count="1" type="Bedrijfsauto Licht" />
                    <category count="1" type="Bedrijfsauto Zwaar" />
                </numberOfInputValuesUsed>
            </travelTimeData>
            <travelTimeData travelTimeType="processed" dataQuality="100.000000" estimationType="estimated">
                <travelTime>123</travelTime>
                <trafficSpeed>12</trafficSpeed>
            </travelTimeData>
        </siteMeasurements>
        <siteMeasurements>
            <measurementSiteReference id="SEC_294" version="1.0">
                <measurementSiteName>Surinameplein</measurementSiteName>
                <measurementSiteType>section</measurementSiteType>
                <length>750</length>
            </measurementSiteReference>
            <travelTimeData travelTimeType="raw" numberOfInputValuesUsed="1">
                <travelTime>123</travelTime>
                <trafficSpeed>12</trafficSpeed>
                <numberOfInputValuesUsed>
                    <category count="1" type="Auto" />
                </numberOfInputValuesUsed>
            </travelTimeData>
            <travelTimeData travelTimeType="representative" numberOfInputValuesUsed="1">
                <travelTime>123</travelTime>
                <trafficSpeed>12</trafficSpeed>
                <numberOfInputValuesUsed>
                    <category count="1" type="Auto" />
                </numberOfInputValuesUsed>
            </travelTimeData>
            <travelTimeData travelTimeType="processed" dataQuality="66.000000" estimationType="estimated">
                <travelTime>137</travelTime>
                <trafficSpeed>19</trafficSpeed>
            </travelTimeData>
        </siteMeasurements>
        <siteMeasurements>
            <measurementSiteReference id="SEC_295" version="1.0">
                <measurementSiteName>Surinameplein</measurementSiteName>
                <measurementSiteType>section</measurementSiteType>
                <length>123</length>
            </measurementSiteReference>
            <travelTimeData travelTimeType="raw">
                <travelTime>-1</travelTime>
                <trafficSpeed>-1</trafficSpeed>
            </travelTimeData>
            <travelTimeData travelTimeType="representative">
                <travelTime>-1</travelTime>
                <trafficSpeed>-1</trafficSpeed>
            </travelTimeData>
            <travelTimeData travelTimeType="processed" dataQuality="3.000000" estimationType="estimated">
                <travelTime>123</travelTime>
                <trafficSpeed>12</trafficSpeed>
            </travelTimeData>
        </siteMeasurements>
    </payloadPublication>
</amsterdamTravelTimes>
"""
