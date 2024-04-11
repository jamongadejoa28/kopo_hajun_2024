package BattleGame;

import java.util.Random;

public class Character1 extends Base {

	/*
	 * 1.캐릭터의 이름은 한글로 세글자로 작성해주세요.(필수는 아님 하지만 글자수를 맞춰야함)
	 * 2.공격에 의해 체력이 닳게 할꺼면 꼭 체력이 감소되게 작성해주세요. -처리
	 */
	public Character1() {
		this.name = "김유신";
	}
	public Character1(String name) {
		this.name = name;
	}
	
	@Override
	public void underAttack() {
		System.out.println(this.name+"공격당함");
		Random random = new Random();
		int attckNum = random.nextInt(2);
		if(attckNum == 0) {
			System.out.println("동상에 걸렸습니다. 체력이 5 감소합니다.");
			this.hp -=5;
		}else {
			System.out.println(this.name+" 캐릭터의 고유 효과로 방어에 성공했습니다.");
		}

	}
	
}
