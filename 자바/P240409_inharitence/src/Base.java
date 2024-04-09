
public class Base {
	String name;
	double resultSize;
	Base(){
		this.name = "기본도형";
	}
	
	//굳이 왜 있어야 하나?
	//doAction사용을 위해
	public void inputSize() {
		//사이즈 입력 메서드
	}
	
	public void calcSize() {
		//도형의 넓이 계산 메서드
	}
	
	public void printSize() {
		//결과출력 메서드
		System.out.println(this.name + "의 영역 크기" + this.resultSize);
	}
	
	public void doAction() {
		this.inputSize();
		this.calcSize();
		this.printSize();
	}
}
