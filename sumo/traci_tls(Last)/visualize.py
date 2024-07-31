import os
import sys
import subprocess

# SUMO_HOME 환경 변수 설정 (필요한 경우)
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Please declare environment variable 'SUMO_HOME'")

# plotXMLAttributes.py 스크립트 경로
plot_script = os.path.join(tools, 'visualization', 'plotXMLAttributes.py')

# E2 detector 출력 파일 경로
e2_output_file = "경로지정"

# 시각화하려는 속성 선택
attributes = [("meanOccupancy", "Occupancy"), ("meanSpeed", "Mean Speed"), ("nVehSeen", "Vehicle Count")]

# 각 속성에 대한 그래프 생성
for attr, label in attributes:
    output_file = f"e2_detector_{attr}_plot.png"
    cmd = [
        sys.executable,  # Python interpreter
        plot_script,
        e2_output_file,
        "-x", "begin",
        "-y", attr,
        "--labels", f"E2 Detector {label}",
        "--xlabel", "Simulation Time (s)",
        "--ylabel", label,
        "--title", f"E2 Detector {label} over Time",
        "-o", output_file,  # 출력 파일 지정
        "-b"  # 그래프를 화면에 표시하지 않고 파일로만 저장
    ]

    print(f"Generating plot for {label}...")
    try:
        # 서브프로세스로 plotXMLAttributes.py 실행
        subprocess.run(cmd, check=True)
        print(f"Plot saved as {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error generating plot for {label}: {e}")

print("All graphs have been generated.")