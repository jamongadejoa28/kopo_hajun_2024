import java.util.Arrays;

public class RunClass {
	public static void main(String[] args) {
		ClassRoom a = new ClassRoom("A반");
		ClassRoom b = new ClassRoom("B반");
		ClassRoom c = new ClassRoom("C반");
		
		a.setStudent(50);
		b.setStudent(49);
		c.setStudent(40);
		
		System.out.println(Arrays.toString(b.student));
		
		System.out.println(Test.versionCode);
		Test.t1("hi");
	}
}
