#include <graphics.h>
#include <string>
#include <string.h>
#include <filesystem>
#include <random>
#include <vector>
#include<iostream>
#include <windows.h>  // 引入 Win32 API
#define SCREEN_WIDTH 950
#define SCREEN_HEIGHT 550
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
	static std::wstring rf(const std::string& s="F:/"){//形参是文件夹路径，默认是U盘路径
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
class Button{
private:
	int x;
	int y;
	int width;
	int height;
	std::string s;
public:
	Button(int x,int y,int w,int h,std::string s){
		this->x = x;
		this->y = y;
		this->width = w;
		this->height = h;
		this->s = s;
		setcolor(BLACK);
		setfont(40, 0, "楷体");
		xyprintf(200, 220, "%s\n", s);
	}
};
class Manager{
private:
	MUSIC music;
	float volume;//音量
	std::vector<std::wstring> music_list;
public:
	void random_music(){
		std::wstring wstr = Random::rf("F:/");
		// 指定文件夹路径,返回一个文件名【但是要加上.c_str()才能变为一个LPCTSTR类型】
		this->music.OpenFile(wstr.c_str());
		//检查是否打开
		if (this->music.IsOpen()){	
			setcaption(wstr.c_str());
			this->music.Play();
			getch();//MUSIC如果不是全局变量，那就加上这行
		}else{
			//MessageBox(hh, "无法打开该mp3文件！", "打不开", MB_OK | MB_ICONINFORMATION);
			xyprintf(20, 20, "%s\n", "无法打开该mp3文件!");
		}
		this->music.Close();
	}
	void start(){
		initgraph(SCREEN_WIDTH,SCREEN_HEIGHT,0);
		setbkcolor(RGB(250,250,250));
		setcaption("小听歌");
		while(true){
			this->random_music();
			
		}
		this->random_music();
		getch(); // 暂停程序，等待用户按下任意键
		closegraph();
	}  
};
int main(){ 
	Manager m;
	m.start();
	return 0;
}  

