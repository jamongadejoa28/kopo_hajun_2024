#!/usr/bin/env python
# Eclipse SUMO, Simulation of Urban MObility; see https://eclipse.dev/sumo
# Copyright (C) 2009-2024 German Aerospace Center (DLR) and others.
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License 2.0 which is available at
# https://www.eclipse.org/legal/epl-2.0/
# This Source Code may also be made available under the following Secondary
# Licenses when the conditions for such availability set forth in the Eclipse
# Public License 2.0 are satisfied: GNU General Public License, version 2
# or later which is available at
# https://www.gnu.org/licenses/old-licenses/gpl-2.0-standalone.html
# SPDX-License-Identifier: EPL-2.0 OR GPL-2.0-or-later

# @file    runner.py
# @author  Lena Kalleske
# @author  Daniel Krajzewicz
# @author  Michael Behrisch
# @author  Jakob Erdmann
# @date    2009-03-26

#!/usr/bin/env python

import os
import sys
import optparse
import random
import numpy as np
from collections import defaultdict


# SUMO 환경 설정
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

from sumolib import checkBinary
import traci


def get_time_factor(step):
    hour = (step//60) % 24
    if 7 <= hour < 9 or 17 <= hour < 19:
        return 2.0  # 출퇴근 시간대 교통량 증가
    return 1.0


def generate_routefile():
    np.random.seed(42)
    N = 3600  #
    lambda_routes = {
        'right': 1. / 7,
        'left': 1. / 7,
        'down': 1. / 5,
        'up': 1. / 5,
        'turn_left1': 1. / 10,
        'turn_left2': 1. / 10,
        'turn_left3': 1. / 10,
        'turn_left4': 1. / 10,
        'turn_right1': 1. / 11,
        'turn_right2': 1. / 11,
        'turn_right3': 1. / 11,
        'turn_right4': 1. / 11
    }

    with open("data/cross.rou.xml", "w") as routes:
        print("""<routes>
        <vType id="car" accel="0.8" decel="4.5" sigma="0.5" length="5" minGap="2.5" maxSpeed="100" guiShape="passenger" />
        <vType id="bus" accel="0.8" decel="4.5" sigma="0.5" length="12" minGap="3" maxSpeed="80" guiShape="bus" />

        <route id="right" edges="51o 1i 2o 52i" />
        <route id="left" edges="52o 2i 1o 51i" />
        <route id="down" edges="54o 4i 3o 53i" />
        <route id="up" edges="53o 3i 4o 54i" />

        <route id="turn_left1" edges="51o 1i 4o 54i" />
        <route id="turn_left2" edges="52o 2i 3o 53i" />
        <route id="turn_left3" edges="53o 3i 1o 51i" />
        <route id="turn_left4" edges="54o 4i 2o 52i" />

        <route id="turn_right1" edges="51o 1i 3o 53i" />
        <route id="turn_right2" edges="52o 2i 4o 54i" />
        <route id="turn_right3" edges="53o 3i 2o 52i" />
        <route id="turn_right4" edges="54o 4i 1o 51i" />
        """, file=routes)

        vehNr = 0
        vehicleType = ["car", "bus"]
        for step in range(N):
            time_factor = get_time_factor(step)
            for route, lambda_val in lambda_routes.items():
                route = random.choice(list(lambda_routes.keys()))
                veh_type = random.choice(vehicleType)
                if random.uniform(0, 1) < lambda_val * time_factor:
                    print(
                        f'<vehicle id="{veh_type}_{vehNr}" type="{veh_type}" route="{route}" depart="{step}" departLane="random"/>',
                        file=routes)
                    vehNr += 1
        print("</routes>", file=routes)

# E2 detector 설정
e2_detectors = {
    'horizontal': ['e2_5', 'e2_6', 'e2_7', 'e2_8', 'e2_3', 'e2_4', 'e2_12', 'e2_13'],
    'vertical': ['e2_0', 'e2_1', 'e2_2', 'e2_9', 'e2_10', 'e2_11', 'e2_14', 'e2_15']
}


def is_congested(detector_id):
    return traci.lanearea.getLastStepOccupancy(detector_id) >= 60


def get_congested_directions(e2_detectors):
    congested_directions = {
        'horizontal': False,
        'vertical': False
    }

    horizontal_detectors = e2_detectors['horizontal']
    vertical_detectors = e2_detectors['vertical']

    if all(is_congested(det) for det in horizontal_detectors):
        congested_directions['horizontal'] = True
    if all(is_congested(det) for det in vertical_detectors):
        congested_directions['vertical'] = True

    return congested_directions


def get_yellow_phase_duration(tl_id, phase_index):
    logic = traci.trafficlight.getCompleteRedYellowGreenDefinition(tl_id)[0]
    return logic.phases[phase_index].duration


def set_yellow_phase(tl_id):
    current_phase = traci.trafficlight.getPhase(tl_id)
    if current_phase == 0:  # 수평 방향 녹색
        yellow_phase = 1  # 수평 방향 황색
    elif current_phase == 2:  # 수직 방향 녹색
        yellow_phase = 3  # 수직 방향 황색
    else:
        return  # 이미 황색이거나 적색 상태

    traci.trafficlight.setPhase(tl_id, yellow_phase)
    yellow_duration = get_yellow_phase_duration(tl_id, yellow_phase)
    return yellow_duration


def set_green_phase(tl_id, direction):
    current_phase = traci.trafficlight.getPhase(tl_id)
    if direction == 'horizontal' and current_phase != 0:
        if current_phase != 1:
            yellow_duration = set_yellow_phase(tl_id)
            if yellow_duration:
                traci.simulationStep(traci.simulation.getTime() + yellow_duration)
        traci.trafficlight.setPhase(tl_id, 0)  # 수평 방향 녹색
    elif direction == 'vertical' and current_phase != 2:
        if current_phase != 3:
            yellow_duration = set_yellow_phase(tl_id)
            if yellow_duration:
                traci.simulationStep(traci.simulation.getTime() + yellow_duration)
        traci.trafficlight.setPhase(tl_id, 2)  # 수직 방향 녹색


def control_traffic_lights(tl_id, e2_detectors):
    congested_directions = get_congested_directions(e2_detectors)

    if congested_directions['vertical'] and congested_directions['horizontal']:
        set_green_phase(tl_id, 'vertical')
    elif congested_directions['vertical']:
        set_green_phase(tl_id, 'vertical')
    elif congested_directions['horizontal']:
        set_green_phase(tl_id, 'horizontal')

def run(tl_id, e2_detectors):
    step = 0
    bus_data = defaultdict(list)
    car_data = defaultdict(list)

    try:
        while traci.simulation.getMinExpectedNumber() > 0:
            traci.simulationStep()

            for vehicle_id in traci.vehicle.getIDList():
                current_edge = traci.vehicle.getRoadID(vehicle_id)
                edge_length = traci.lane.getLength(f"{current_edge}_0")
                vehicle_pos = traci.vehicle.getLanePosition(vehicle_id)
                veh_type = traci.vehicle.getTypeID(vehicle_id)
                travel_time = traci.vehicle.getAccumulatedWaitingTime(vehicle_id)
                if veh_type == "bus":
                    if vehicle_pos >= 0.65 * edge_length:
                        traci.vehicle.setLaneChangeMode(vehicle_id, 0)
                    bus_data[vehicle_id].append(travel_time)
                else:
                    car_data[vehicle_id].append(travel_time)
            control_traffic_lights(tl_id, e2_detectors)

            step += 1
    finally:
        if bus_data:
            avg_bus_time = sum([max(times) for times in bus_data.values()]) / len(bus_data)
            print(f"Average bus travel time: {avg_bus_time:.2f} seconds")
        else:
            print("No bus data available")

        if car_data:
            avg_car_time = sum([max(times) for times in car_data.values()]) / len(car_data)
            print(f"Average car travel time: {avg_car_time:.2f} seconds")
        else:
            print("No car data available")
def get_options():
    optParser = optparse.OptionParser()
    optParser.add_option("--nogui", action="store_true", default=False, help="run the commandline version of sumo")
    options, args = optParser.parse_args()
    return options

if __name__ == "__main__":
    options = get_options()
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(current_dir, "output")

    # output 디렉토리가 없으면 생성
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")

    generate_routefile()

    sumoCmd = [sumoBinary, "-c", "data/cross.sumocfg", "--tripinfo-output", "tripinfo.xml"]

    try:
        traci.start(sumoCmd)
        tl_id = "0"
        run(tl_id, e2_detectors)
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        try:
            traci.close()
        except:
            pass

