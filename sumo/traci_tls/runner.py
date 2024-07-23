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

from detector_analyzer import DetectorAnalyzer

# SUMO 환경 설정
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

from sumolib import checkBinary
import traci

def generate_routefile():
    np.random.seed(42)
    N = 3600  # number of time steps
    # demand per second from different directions
    lambda_routes = {
        'right': 1. / 15,
        'left': 1. / 15,
        'down': 1. / 35,
        'up': 1. / 35,
        'turn_left1': 1. / 25,
        'turn_left2': 1. / 25,
        'turn_left3': 1. / 25,
        'turn_left4': 1. / 25,
        'turn_right1': 1. / 30,
        'turn_right2': 1. / 30,
        'turn_right3': 1. / 30,
        'turn_right4': 1. / 30
    }

    with open("data/cross.rou.xml", "w") as routes:
        print("""<routes>
        <vType id="typeWE" accel="0.8" decel="4.5" sigma="0.5" length="5" minGap="2.5" maxSpeed="16.67" guiShape="passenger"/>
        <vType id="typeNS" accel="0.8" decel="4.5" sigma="0.5" length="7" minGap="3" maxSpeed="25" guiShape="bus"/>

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
        vehicle_types = ["typeWE", "typeNS"]
        all_routes = list(lambda_routes.keys())

        for i in range(N):
            for route, lambda_val in lambda_routes.items():
                if random.random() < lambda_val:
                    vehicle_type = random.choice(vehicle_types)
                    depart_lane = "random"
                    print(f'<vehicle id="{route}_{vehNr}" type="{vehicle_type}" route="{route}" depart="{i}" departLane="{depart_lane}"/>', file=routes)
                    vehNr += 1
        print("</routes>", file=routes)


def get_route_info():
    routes = {}
    for route_id in traci.route.getIDList():
        edge_ids = traci.route.getEdges(route_id)
        routes[route_id] = {
            'edges': edge_ids,
            'lanes': [
                {
                    'edge_id': edge_id,
                    'lane_ids': [f"{edge_id}_{i}" for i in range(traci.edge.getLaneNumber(edge_id))],
                    'lane_indexes': list(range(traci.edge.getLaneNumber(edge_id)))
                }
                for edge_id in edge_ids
            ]
        }
    return routes


def get_turn_type(route_id):
    if "turn_left" in route_id:
        return "left"
    elif "turn_right" in route_id:
        return "right"
    else:
        return "straight"


def get_correct_lane(vehicle_id, route_id, current_edge, routes):
    turn_type = get_turn_type(route_id)
    lanes = len(routes[route_id]['lanes'][1]['lane_ids'])  # 진입 도로의 차선 수

    if turn_type == "left":
        return lanes - 1  # 가장 왼쪽 차선
    elif turn_type == "right":
        return 0  # 가장 오른쪽 차선
    else:
        return random.choice([1, 2])  # 중간 두 차선 중 랜덤 선택


def check_and_change_lane(vehicle_id, route_id, routes):
    route = routes[route_id]
    current_edge = traci.vehicle.getRoadID(vehicle_id)

    if current_edge == route['edges'][1]:  # 진입 도로에 있는 경우
        vehicle_lane = traci.vehicle.getLaneIndex(vehicle_id)
        correct_lane = get_correct_lane(vehicle_id, route_id, current_edge, routes)

        print(f"Before lane change - Vehicle ID: {vehicle_id}, Route: {route_id}, Edge: {current_edge}, Lane: {vehicle_lane}")

        if vehicle_lane != correct_lane:
            traci.vehicle.setLaneChangeMode(vehicle_id, 0)  # 자동 차선 변경 비활성화
            traci.vehicle.moveTo(vehicle_id, f"{current_edge}_{correct_lane}",
                                 traci.vehicle.getLanePosition(vehicle_id))
            traci.vehicle.setLaneChangeMode(vehicle_id, 1621)  # 차선 변경 모드 복원

            new_lane = traci.vehicle.getLaneIndex(vehicle_id)
            print(f"After lane change - Vehicle ID: {vehicle_id}, Route: {route_id}, Edge: {current_edge}, Lane: {new_lane}")

def get_lane_density(lane_id):
    return traci.lane.getLastStepVehicleNumber(lane_id) / traci.lane.getLength(lane_id)

def control_traffic_lights():
    for tl_id in traci.trafficlight.getIDList():
        program = traci.trafficlight.getAllProgramLogics(tl_id)[0]
        current_phase_index = traci.trafficlight.getPhase(tl_id)
        current_phase_duration = program.phases[current_phase_index].duration

        if traci.simulation.getTime() % current_phase_duration == 0:
            incoming_lanes = traci.trafficlight.getControlledLanes(tl_id)
            lane_densities = [get_lane_density(lane) for lane in incoming_lanes]
            max_density_index = lane_densities.index(max(lane_densities))

            # 가장 혼잡한 차선에 대해 녹색 신호 시간 연장
            if max_density_index == current_phase_index:
                extended_duration = min(current_phase_duration * 1.5, 90)  # 최대 90초로 제한
                traci.trafficlight.setPhaseDuration(tl_id, extended_duration)
            else:
                next_phase_index = (current_phase_index + 1) % len(program.phases)
                traci.trafficlight.setPhase(tl_id, next_phase_index)


def run():
    step = 0
    changed_vehicles = set()
    routes = get_route_info()

    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()

        for vehicle_id in traci.vehicle.getIDList():
            if vehicle_id not in changed_vehicles:
                route_id = traci.vehicle.getRouteID(vehicle_id)
                current_edge = traci.vehicle.getRoadID(vehicle_id)

                if current_edge == routes[route_id]['edges'][1]:  # 진입 도로에 있는 경우
                    edge_length = traci.lane.getLength(f"{current_edge}_0")  # 첫 번째 차선의 길이
                    vehicle_pos = traci.vehicle.getLanePosition(vehicle_id)

                    if vehicle_pos >= 0.15 * edge_length:  # 도로 길이의 15%를 지났을 때
                        check_and_change_lane(vehicle_id, route_id, routes)
                        changed_vehicles.add(vehicle_id)

        # 신호등 제어 로직 (유연한 동작을 위해 추가 구현 필요)
        control_traffic_lights()

        step += 1

# def analyze_data():
#     print("Analyzing detector data...")
#     current_dir = os.path.dirname(os.path.abspath(__file__))
#
#     print("Files in data directory:")
#     data_dir = os.path.join(current_dir, 'data')
#     for file in os.listdir(data_dir):
#         print(f"  {file}")
#
#     analyzer = DetectorAnalyzer(current_dir)
#     analyzer.print_table()
#     analyzer.save_table_to_csv()

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
        run()
    except traci.exceptions.TraCIException as e:
        print(f"TraCI exception: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        try:
            traci.close()
        except:
            pass

    # 시뮬레이션 종료후 자동으로 데이터프레임 만들기 함수 실행하려면 다시 활성화
    # analyze_data()

