package BattleGame;

public class MainClass {
	public static void main(String[] args) {
		
		Base characters[] = new Base[5];
		
		characters[0] = new Character1("김선호");
		characters[1] = new Character1("전상문");
		characters[2] = new Character1("김태훈");
		characters[3] = new Character1("김유경");
		characters[4] = new Character1("조하준"); // 여기에 본인이 만든 캐릭터 넣어주면됩니다!!!
		
		
		Game game = new Game(characters); // 게임
		
//		game.showCurrCharacter();
		
		System.out.println("게임을 시작합니다.");
		
		game.play();
		game.showCurrGame();
		game.play();
		game.showCurrGame();
		game.play();
		game.showCurrGame();
		game.play();
		game.showCurrGame();
	}
}
