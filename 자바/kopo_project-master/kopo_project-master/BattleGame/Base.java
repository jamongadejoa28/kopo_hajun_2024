package BattleGame;

public abstract class Base {
	String name;
	int hp;
	
	Base(){
		this.name = "기본 캐릭터";
		this.hp = 100;
	}
	
	public abstract void underAttack();
	
	
	public boolean isLive() {
		return this.hp > 1;
	}
}
