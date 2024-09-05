#include <graphics.h>
#include <string.h>
#include <math.h>

class ProgressBar
{
private:
	//进度条样式参数
	int x, y, width, height;	//位置，尺寸
	color_t progressBkcolor;	//进度条背景色
	color_t progressColor;		//进度条进度颜色
	float progress;				//进度
	
public:
	ProgressBar(int x, int y, int width, int height) : x(x), y(y), width(width), height(height) {
		progressBkcolor = LIGHTGRAY;
		progressColor = LIGHTBLUE;
		progress = 0.0f;
	}
	
	void setProgress(float progress) {
		this->progress = progress;
		draw();
	}
	
private:
	void draw() {
		int cur = (int)(x + width * progress);
		
		setfillcolor(progressColor);
		bar(x, y, cur, y + height);
		setfillcolor(progressBkcolor);
		bar(cur, y, x + width, y + height);
	}
};

int main()
{
	initgraph(640, 480, INIT_RENDERMANUAL);
	setcaption("EGE音乐播放");	
	setbkcolor(WHITE);
	setcolor(BLACK);
	xyprintf(20, 20, "按空格键播放/暂停， S 键停止");
	xyprintf(20, 40, "P键增大音量，M键减小音量");
	xyprintf(20, 60, "N键前进，B键后退");
	xyprintf(20, 80, "Q键退出");
	setcolor(LIGHTBLUE);
	//手动渲染模式，先刷新一下窗口，让背景色先出来
	//因为音乐加载需要时间，这段时间窗口是黑色的
	delay_ms(0);
	MUSIC music;
	//音乐文件名
	const char* musicFile = "F:/BEYOND - 海阔天空.mp3";
	//找歌名位置
	int len = strlen(musicFile);
	while (len >= 0 && musicFile[len] != '/' && musicFile[len] != '\\') {
		--len;
	}
	const char* musicName = musicFile + len + 1;
	music.OpenFile(musicFile);
	
	if (music.IsOpen()) {
		ProgressBar progressBar(20, 200, 500, 20);
		progressBar.setProgress(0.0f);
		
		music.Play(0);
		
		int playTime = 0;				
		int totalTime = music.GetLength();		//获取音乐总时长(单位：毫秒）
		float volume = 0.8f;					//音量	
		music.SetVolume(volume);
		
		xyprintf(20, 160, "音乐名：%s", musicName);
		xyprintf(400, 240, "音乐总时长:%02d:%02d",
			totalTime / 1000 / 60, totalTime / 1000 % 60);
		
		bool exit = false;
		
		//上次调节进度时间
		double lastAdjustTime = fclock(), curtime = lastAdjustTime;
		
		//检测键盘，控制音乐播放
		for (; is_run(); delay_fps(20)) {
			if (exit)
				break;
			
			while (kbmsg()) {
				key_msg keyMsg = getkey();
				if (keyMsg.msg != key_msg_down)
					continue;
				
				DWORD status = music.GetPlayStatus();
				int key = keyMsg.key;
				switch (key) {
					case 'Q':		//退出
					exit = true;
					break;
					case ' ':		//播放暂停切换
					if (status == MUSIC_MODE_PLAY)
						music.Pause();
					else if (status == MUSIC_MODE_PAUSE)
						music.Play();
					else if (status == MUSIC_MODE_STOP)
						music.Play(0);
					
					break;
					case 'S':		//停止
					if (status != MUSIC_MODE_STOP) {	
						music.Play(0);
						music.Stop();
					}
					break;
					
					case 'P':		//增加音量
					if ((volume += 0.1f) >= 1)
						volume = 1;
					music.SetVolume(volume);
					break;
					case 'M':		//减小音量
					if ((volume -= 0.1f) < 0)
						volume = 0;
					music.SetVolume(volume);
					break;
					case 'N':		//快进
					//no-break;
					case 'B':		//快退
					curtime= fclock();
					if (curtime- lastAdjustTime < 0.3)
						break;
					lastAdjustTime = curtime;
					
					if (key == 'N') {
						playTime += 10 * 1000;
						if (playTime > totalTime)
							playTime = totalTime;
					}
					else {
						playTime -= 10 * 1000;
						if (playTime < 0)
							playTime = 0;
					}
					music.Play(playTime);
					break;
				}
			}
			//获取播放时间（毫秒）
			int pos = music.GetPosition();
			
			//更新进度条
			if (pos != playTime) {
				playTime = pos;
				progressBar.setProgress(playTime * 1.0f / totalTime);
			}
			xyprintf(20, 240, "播放进度%02d:%02d", playTime / 1000 / 60, playTime / 1000 % 60);
			xyprintf(20, 280, "音量%3.0f%%", (volume * 100));
		}
		
		//关闭音乐
		music.Close();
	}
	else {
		xyprintf(50, 200, "打开音乐失败,请检查音乐文件名");
		getch();
	}
	
	closegraph();
	
	return 0;
}

