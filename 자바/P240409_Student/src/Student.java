
public class Student {
	private String name;
	int middleScore;
	int finalScore;
	int totalScore;
	
	Student() {
		
	}
	
	Student(String name) {
		this.name = name;
	}
	
	Student(String name, int middleScore, int finalScore) {
		this.name = name;
		this.middleScore = middleScore;
		this.finalScore = finalScore;
		this.totalScore = middleScore + finalScore;
	}
	
	public String toString() {
		return this.name + " (중간: "
				+ this.middleScore + ", 기말: "
				+ this.finalScore + ", 총합: "
				+ this.totalScore + ")";
	}
	
//	public void setName(String name) {
//		this.name = name;
//	}
//	
//	public String getName() {
//		return this.name;
//	}
//	
//	public void setMiddleScore(int middleScore) {
//		this.middleScore = middleScore;
//	}
//	
//	public int getMiddleScore() {
//		return this.middleScore;
//	}
//	
//	public void setFinalScore(int finalScore) {
//		this.finalScore = finalScore;
//	}
//	
//	public int getFinalScore() {
//		return this.finalScore;
//	}
//	
//	public void setTotalScore(int totalScore) {
//		this.totalScore = totalScore;
//	}
//	
//	public int getTotalScore() {
//		return this.totalScore;
//	}
}


