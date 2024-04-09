import java.util.Scanner;

public class Triangle extends Base{
	int width;
	int height;
	
	Triangle(){
		this.name = "삼각형";
	}
	
	@Override
	public void inputSize() {
		Scanner scanner = new Scanner(System.in);
		System.out.println("Width: ");
		String inputText = scanner.nextLine();
		this.width = Integer.parseInt(inputText);
		System.out.println("Height: ");
		inputText = scanner.nextLine();
		this.height = Integer.parseInt(inputText);
	}
	
	@Override
	public void calcSize() {
		this.resultSize = width * height / (double)2;
	}
}
