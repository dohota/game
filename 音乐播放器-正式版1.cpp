#include <graphics.h>
#include <string>
#include <string.h>
#include <filesystem>
#include <random>
#include <vector>
#include <iostream>
#include <windows.h>  // 引入 Win32 API
#include <functional>

#define SCREEN_WIDTH 950
#define SCREEN_HEIGHT 550
MUSIC music;

class Random{
public:
	static int r(int a,int b){
		std::random_device rd; // 随机数种子
		std::mt19937 gen(rd()); // 使用Mersenne Twister 19937算法生成随机数引擎
		std::uniform_real_distribution<double> dis(0.0, 1.0); // 定义在[0, 1)范围内的均匀分布随机数
		double random = dis(gen); // 生成0到1之间的随机数
		return random *(b-a) +a;
	}
	static std::wstring stringToWstring(const std::string& str) {  
		int size_needed = MultiByteToWideChar(CP_UTF8, 0, &str[0], (int)str.size(), NULL, 0);  
		std::wstring wstrTo(size_needed, 0);  
		MultiByteToWideChar(CP_UTF8, 0, &str[0], (int)str.size(), &wstrTo[0], size_needed);  
		return wstrTo;  
	}
	static std::wstring rf(const std::string& s){//形参是文件夹路径，默认是U盘路径
		std::vector<std::string> mp3Files;
		for (const auto& entry : std::filesystem::directory_iterator(s)) {
			if (entry.path().extension() == ".mp3") {
				mp3Files.push_back(entry.path().filename().string());
			}
		}	
		if (mp3Files.empty()) {
			//MessageBox(hh, "该文件夹里没有mp3文件！", "无文件", MB_OK | MB_ICONINFORMATION);
			xyprintf(20, 20, "%s\n", "文件夹里没有mp3文件啊");
			return std::wstring();
		}else{
			std::random_device rd;
			std::mt19937 gen(rd());
			std::uniform_int_distribution<> dis(0, mp3Files.size() - 1);
			int randomIndex = dis(gen);
			std::wstring wstr = Random::stringToWstring(s+mp3Files[randomIndex]);
			//如果项目用Unicode,那么LPCTSTR等同于const wchar_t*
			return wstr;	
		}	
	}
};

class Shape{
private:
	static void triangle(int x1,int y1,int x2,int y2,int x3,int y3){
		int p[6];
		p[0]=x1;
		p[1]=y1;
		p[2]=x2;
		p[3]=y2;
		p[4]=x3;
		p[5]=y3;
		setfillcolor(BLACK);
		fillpoly(3,p);
	}
public:
	static void draw_shape(std::string shape_name,int x,int y,int w=50,int h=40){
	//把图形画在按钮里面，所以要知道按钮的数据
		if(shape_name == "add"){
			//用两根粗线画一个十字
			setlinewidth(5);
			line(x+w/5,y+h/2,x+w-w/5,y+h/2);
			setlinewidth(5);
			line(x+w/2,y+h/5,x+w/2,y+h-h/5);
		}else if(shape_name == "minus"){
			setlinewidth(5);
			line(x+w/4,y+h/2,x+w-w/4,y+h/2);
		}else if(shape_name == "next"){
			//画两个三角形，其中一个是另一个的一半，基本居中
			int ww =w/2;
			Shape::triangle(x+ww/4,y+h/4,x+ww/4,y+h-h/4,x+ww,y+h/2);//big
			Shape::triangle(x+ww,y+3*h/8,x+ww,y+5*h/8,x+w-ww/4,y+h/2);//small
		}else if(shape_name == "last"){
			//翻转“next”的两个三角形
			int ww =w/2;
			Shape::triangle(x+ww,y+3*h/8,x+ww,y+5*h/8,x+ww/4,y+h/2);//small
			Shape::triangle(x+w-ww/4,y+h/4,x+w-ww/4,y+h-h/4,x+ww,y+h/2);//big
		}else if(shape_name == "continue"){
			//画一个基本居中的三角形
			Shape::triangle(x+w/4,y+h/4,x+w/4,y+h-h/4,x+w-w/4,y+h/2);
		}else if(shape_name == "pause"){
			//画两根竖着的粗实线
			setlinewidth(4);
			line(x+w/3,y+h/5,x+w/3,y+h-h/5);
			setlinewidth(4);
			line(x+w-w/3,y+h/5,x+w-w/3,y+h-h/5);
		}
	}
};

class SlideBar{
private:
	int x;
	int y;
	int w;
	int h;
	float progress;
public:
	bool rr;
	SlideBar(int x,int y,int w,int h){
		this->x = x;
		this->y = y;
		this->w = w;
		this->h = h;
		this->progress = 0.0f;
	}
	void change(float progress){
		//进度条可能是随着歌曲播放自动改变，也可以是手动点击改变
		this->progress = progress;
		int cur = (int)(this->x+this->w*progress);
		setfillcolor(RED);
		bar(x,y,cur,y+h);//进度条
		setfillcolor(BLACK);
		bar(cur,y,x+w,y+h);//总刻度-进度条
	}
	float change2(int mx,int my){
		if(mx >= x && mx <= x+w && my >= y && my<=y+h){
			this->rr = true;
			float progress = (mx-x)*1.0f / w;
			this->change(progress);
			return progress;
		}else{
			this->rr = false;
			return 0;
		}
	}
};

class Button{
private:
	int x;
	int y;
	int w;
	int h;
	int s;
	std::string type;
public:
	Button(int x,int y,std::string button_type,int w=80,int h=60){
		this->x = x;
		this->y = y;
		this->w = w;
		this->h = h;
		this->type = button_type;
	}
	void draw(){
		setbkcolor(WHITE);//填充矩形的颜色
		bar(x,y,x+w,y+h);//画无边框填充矩形
		Shape::draw_shape(this->type,this->x,this->y);
	}
	void change(std::function<void()> callback,int px,int py){
		if(px >= x && px <= x+w && py >= y && py <= y+h){//鼠标点击按钮的范围
			if(this->type == "continue"){
				this->type = "pause";
				this->draw();
			}
			if(this->type == "pause"){
				this->type = "continue";
				this->draw();
			}
			callback();
		}
	}
};

class Manager{
private:
	float volume;//音量
	int playtime;//一首歌进度条上的理论时间，正常应与真实时间相同
	int pt;//一首歌真实的播放时间
	int totaltime;//一首歌总时间
	unsigned index;//播放列表里的第几首歌
	std::vector<std::wstring> music_list;

public:
	void add_volume(){
		if(this->volume >=1){
			this->volume = 1;
		}else{
			this->volume += 0.1f;
		}
		music.SetVolume(this->volume);
	}
	void minus_volume(){
		if(this->volume <= 0){
			this->volume = 0;
		}else{
			this->volume -= 0.1f;
		}
		music.SetVolume(this->volume);
	}
	void change_pause(){
		DWORD status = music.GetPlayStatus();
		if (status == MUSIC_MODE_PLAY){
			music.Pause();
		}
		else if (status == MUSIC_MODE_PAUSE){
			music.Play();		
		}
	}
	void last_song(){
		if(this->index >0){
			//第一首歌之前就没歌了
			music.Close();
			this->index -= 1;
			music.OpenFile(this->music_list[this->index].c_str());
			setcaption(this->music_list[this->index].c_str());
			this->play_music();
		}
	}
	void next_song(){
		music.Close();
		if(this->music_list.size() == this->index + 1){//下一首随机
			this->index += 1;
			this->choose_random_music();
			this->play_music();
		}else{
			this->index +=1;
			music.OpenFile(this->music_list[this->index].c_str());
			setcaption(this->music_list[this->index].c_str());
			this->play_music();
		}
	}
	
	void changel(float progress){
		this->playtime = int(progress* this->totaltime);
		music.Play(this->playtime);//this->playtime本身单位就是毫秒
	}
	void choose_random_music(){
		std::wstring wstr = Random::rf("F:/");
		// 指定文件夹路径,返回一个文件名【但是要加上.c_str()才能变为一个LPCTSTR类型】
		music.OpenFile(wstr.c_str());
		setcaption(wstr.c_str());
		this->music_list.push_back(wstr.c_str());
	}
	void play_music(){
		if (music.IsOpen()){
			this->playtime = 0;
			this->totaltime = music.GetLength();
			music.Play(0);
			//getch();//MUSIC如果不是全局变量，那就加上这行
		}else{
			//MessageBox(hh, "无法打开该mp3文件！", "打不开", MB_OK | MB_ICONINFORMATION);
			xyprintf(20, 20, "%s\n", "无法打开该mp3文件!");
		}
	}
	
	void start(){
		initgraph(SCREEN_WIDTH,SCREEN_HEIGHT,0);
		setbkcolor(YELLOWGREEN);
		setcaption("小型听歌软件");
		setcolor(RED);
		this->volume = 0.4;//初始音量
		this->index = 0;
		Manager* manager;
		std::function<void()> callback1 = [&manager]() { manager->last_song(); };
		std::function<void()> callback2 = [&manager]() { manager->change_pause(); };
		std::function<void()> callback3 = [&manager]() { manager->next_song(); };
		std::function<void()> callback4 = [&manager]() { manager->add_volume(); };
		std::function<void()> callback5 = [&manager]() { manager->minus_volume(); };
		//上面示例的lanmda表达式中，&manager是指向 Manager类对象指针
		SlideBar sb(100,SCREEN_HEIGHT/2,SCREEN_WIDTH-200,10);
		Button b1(SCREEN_WIDTH/2 -80,9*SCREEN_HEIGHT/10,"last",90,80);
		Button b2(SCREEN_WIDTH/2,9*SCREEN_HEIGHT/10,"pause",90,80);
		//一开始歌曲默认为播放状态,所以显示暂停图标
		Button b3(SCREEN_WIDTH/2 +80,9*SCREEN_HEIGHT/10,"next",90,80);
		Button b4(10,SCREEN_HEIGHT/2,"add");
		Button b5(10,SCREEN_HEIGHT/2+60,"minus");
		//以上变量都是在栈区申请空间
		this->choose_random_music();
		this->play_music();//单独一个线程运行，所以在循环之外
		for (; is_run(); delay_fps(20)) {
			cleardevice();
			this->pt = music.GetPosition();
			sb.change(0);
			while (mousemsg()) {
				mouse_msg msg = getmouse();
				if (msg.is_left() && msg.is_down()){//按下鼠标左键
					int mx = msg.x;
					int my = msg.y;
					b1.change(callback1,mx,my);
					b2.change(callback2,mx,my);
					b3.change(callback3,mx,my);
					b4.change(callback4,mx,my);
					b5.change(callback5,mx,my);
					float ppp = sb.change2(mx,my);
					if(sb.rr){
						this->changel(ppp);
					}
				}
			}
			while(kbmsg()){
				key_msg kkk = getkey();
				if(kkk.msg!=key_msg_down){
					continue;
				}
				int key = kkk.key;
				switch (key) {
				case 'A':
					this->last_song();
					break;
				case 'D':
					this->next_song();
					break;
				case 'W':
					this->add_volume();
					break;
				case 'S':
					this->minus_volume();
					break;
				default:
					break;
				}
			}
			b1.draw();
			b2.draw();
			b3.draw();
			b4.draw();
			b5.draw();
			xyprintf(20,50,"%s\n","点击w键提高音量");
			xyprintf(20,50+25,"%s\n","点击s键降低音量");
			xyprintf(20,50+25*2,"%s\n","点击a键上一首歌曲");
			xyprintf(20,50+25*3,"%s\n","点击d键下一首歌曲");
			//显示播放时间
			xyprintf(80, SCREEN_HEIGHT/2-20, "%02d:%02d", 
				this->pt/1000/60,this->pt/1000%60);
			//显示总时间
			xyprintf(SCREEN_WIDTH-100, SCREEN_HEIGHT/2-20, "%02d:%02d", 
				this->totaltime / 1000 / 60, this->totaltime / 1000 % 60);
			DWORD d = music.GetPlayStatus();
			//如果音乐已经播放完毕
			if (d == MUSIC_MODE_STOP ) {
				this->next_song();//自动播放 下首歌
				//if(this->index >0){this->last_song();}else{this->next_song();}
			}
			if(this->pt != this->playtime){//进度条随时间变化
				this->playtime = this->pt;
				sb.change(this->playtime * 1.0f / this->totaltime);
			}
			Sleep(10);
		}
		//getch(); // 暂停程序，等待用户按下任意键
	}
	~Manager(){
		closegraph();
	}
};
//MUSIC Manager::music;
//运行程序之前先插上U盘，不然会报错！！
//int main(){Manager m;m.start();return 0;}

