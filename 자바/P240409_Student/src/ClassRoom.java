import java.util.Arrays;
import java.util.Comparator;
import java.util.Random;

public class ClassRoom {
	String name;
	Student[] student;
	
	ClassRoom(String name) {
		this.name = name;
	}
	
	public void setStudent(int numberOfStudents) {
		Random random = new Random();
		this.student = new Student[numberOfStudents];
		
		for (int i = 0; i < student.length; i++) {
			String name = "" + i;
			int middleScore = random.nextInt(1001);
			int finalScore = random.nextInt(1001);
			student[i] = new Student(name, middleScore, finalScore);
		}
		
		Arrays.sort(this.student, new Comparator<Student>() {

			@Override
			public int compare(Student o1, Student o2) {
				return o2.totalScore - o1.totalScore;
			}
		});
	}
}
