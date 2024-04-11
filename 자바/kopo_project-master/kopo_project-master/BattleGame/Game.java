package BattleGame;

import java.util.Random;

public class Game {
	
	final int characterCnt = 5; //팀당 캐릭터 갯수
	
	Base characters[]; //캐릭터들
	Base myTeam[];  // 우리팀
	Base yourTeam[]; // 적팀
	
	boolean myTurn = true; // 우리 턴
	int gameTurnCnt = 0; //게임 턴
	
	Game(Base[] characters){
		this.characters = characters;
		setMyTeam();
		setYourTeam();
	}
	
	/* 우리팀 생성 */
	public void setMyTeam() {
		myTeam = new Base[characterCnt]; // 우리 팀 객체 배열 
		Random random = new Random();
		
		for(int i = 0; i < characterCnt; i++) {
			int characterNum = random.nextInt(characters.length); // 캐릭터수 만큼 랜덤으로 생성
			myTeam[i] = new Character1(characters[characterNum].name);
		}
	}
	
	/* 적팀 생성*/
	public void setYourTeam() {
		yourTeam = new Base[characterCnt]; // 상대 팀 객체 배열
		Random random = new Random(); // 랜덤으로 캐릭터 배정
		
		for(int i = 0; i < characterCnt; i++) {
			int characterNum = random.nextInt(characters.length); // 캐릭터수 만큼 랜덤으로 생성
			yourTeam[i] = new Character1(characters[characterNum].name);
		}
	}
	
	/* 게임 현재 상황 */
	public void showCurrGame() {
	    
		Color.red("---적팀---");
		
		// 적팀  
		int digit = 2;
        for (int j = 0; j < 5; j++) {
            System.out.print("+--------------");
        }
        System.out.println();
       
       
        for (int j = 0; j < 5; j++) {
        	String text =yourTeam[j].name +"(" +yourTeam[j].hp+")"; // 적팀 캐릭터 체력 및 이름
            System.out.printf("|%"+digit+"s"+text+"%-3s"," "," ");
        }
        System.out.println("|");
        
        // 몇턴인지 나타내는곳 
        System.out.println();
        System.out.println("        현재 턴"+gameTurnCnt+"번째입니다.");
        System.out.println();
        
        Color.blue("---우리팀---");
        
    	// 우리팀
     
        for (int j = 0; j < 5; j++) {
            System.out.print("+--------------");
        }
        System.out.println();
        // 이름 나타내는곳
        for (int j = 0; j < 5; j++) {
        	String text =myTeam[j].name +"(" +myTeam[j].hp+")"; // 우리팀 캐릭터 체력 및 이름
            System.out.printf("|%"+digit+"s"+text+"%-3s"," "," ");
        }
        System.out.println("|");
	        
	}
	

	
	// 게임 진행
	public void play() {
		
		// 우리턴일때
		if(myTurn) {
			Random random = new Random();
			int attackNum = random.nextInt(5); // 캐릭터수 만큼 랜덤으로 생성
			yourTeam[attackNum].underAttack();
			myTurn = false;
		}
		
		// 적턴일때
		if(!myTurn) {
			Random random = new Random();
			int attackNum = random.nextInt(5); // 캐릭터수 만큼 랜덤으로 생성
			myTeam[attackNum].underAttack();
			myTurn = true;
		}
		
		gameTurnCnt++;
	}
	
	/* 테스트 코드 */
	public void showCurrCharacter() {
		for(int i = 0; i < characters.length ; i++) {
			System.out.println(characters[i].name);
		}
	}
	public void showCurrTeam() {
		for(int i = 0; i < myTeam.length ; i++) {
			System.out.println(myTeam[i]);			
		}
	}
	/* 테스트 코드 끝 */
}



// 글자 색상 클래스 
class Color{
	/*
	 * ANSI escape 코드를 사용해서 색상 변경
	 */
	static void red(String text) {
		System.out.print("\u001B[31m");
		System.out.println(text);
		System.out.print("\u001B[0m"); // 검정색상
	}
	static void blue(String text) {
		System.out.print("\u001B[34m");
		System.out.println(text);
		System.out.print("\u001B[0m"); // 검정색상
	}
}
