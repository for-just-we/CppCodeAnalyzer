struct Date {
  int d, m, y ;
  void init(int dd, int mm, int yy) {  //对三个成员变量进行初始化
    d = dd;
    m = mm;
    y = yy;
  }
  void print() {  //打印类的具体对象
    cout << y << "-" << m << "-" << d << endl;
  }
};