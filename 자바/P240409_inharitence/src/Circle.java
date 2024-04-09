import java.util.Scanner;

public class Circle extends Base{
	double pi = 3.14;
	int r;
	
	Circle(){
		this.name ="원";
	}
	
	@Override
	public void inputSize() {
		Scanner s = new Scanner(System.in);
		System.out.println("반지름의 길이: ");
		this.r = s.nextInt();
	}
	
	@Override
	public void calcSize() {
		this.resultSize = Math.round(pi * r*r*100)/100.0;
	}
	
}
