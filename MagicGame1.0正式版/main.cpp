#include "num.h"
#include "display.h"
//不抛出异常的函数应该使用 noexcept 通知标准库，避免编译器为了处理异常而作一些额外的工作
class Managemet{
public:	
	Managemet(){
		initgraph(SCREEN_WIDTH,SCREEN_HEIGHT);
		setcaption("Magic World");
		setbkcolor(WHITE);
	}
	void start(){
		Display d;
		Player p(3);
		Display::player.push_back(p);
		//60帧(FPS)
		for (; is_run(); delay_fps(60)){
			cleardevice();  // 清屏
			d.show();
			Sleep(10);	
		}	
	}
	~Managemet(){
		closegraph(); //可以省略ege：：
	}
};	
int main()
{
	Managemet m;
	m.start();
    return 0;
}
//	getch();暂停程序，等待用户按下任意键(除暂停作用外，不建议使用)

