//头文件保护是一种防止头文件被多次包含的技术，旨在避免重复定义错误和提高编译效率
//提高编译速度：减少编译器处理同一个头文件的次数，从而提高编译效率。
//简化依赖管理：确保每个头文件只被处理一次，简化了头文件的包含关系和依赖管理
#ifndef OBJ_H
#define OBJ_H
#endif

#include <graphics.h>
//c++默认给的浅拷贝构造函数
//Person（const Person &p）{
// 成员变量a = p.a;		将非静态成员变量全部复制一遍
//.......}
//深拷贝  成员变量b = new 类型（*p.b)
class Obj{
protected:
	//PIMAGE类型是指向图片的指针
	PIMAGE img ;
	int x;
	int y;
	int width;
	int height; 
	float speed;
	void border();
public:
	char direction;//先把方向调成public
	Obj(PIMAGE img);
	Obj(const Obj &o);
	void move(char k);
	//void display();
	virtual ~Obj();
	//子类的析构函数会自动调用父类的析构函数。这是因为在子类对象被销毁时，会依次调用整个继承链中每个类的析构函数
	//std::vector<bool> is_collision(vector<Obj>);碰撞单独写一个类
};
class Bullet:public Obj{
protected:
	//子弹初始坐标是弹夹的坐标，弹夹的坐标是枪的坐标
	int xx;
	int yy;
	int distance;
	void beyond();
public:
	bool alive;
	using Obj::Obj; // c++11继承父类的构造函数
	Bullet(int xx,int yy,char p_direction);
	Bullet(const Bullet &b);
	void move2(char k);
	void display();
	~Bullet();
};

