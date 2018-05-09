#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>
#include <wchar.h>
#include <stdlib.h>
#include <errno.h>

#include <tuple>
#include <vector>
#include <array>
#include <deque>
#include <list>
#include <forward_list>
#include <stack>
#include <queue>
#include <set>
#include <bitset>
#include <map>
#include <unordered_set>
#include <unordered_map>
#include <memory>

typedef struct st {
	int i;
	unsigned ui;
	long l;
	unsigned long ul;
	float f;
	double d;
} st;

int main(int argc, char* argv[]) { 
	wchar_t *wstr = L"Василий Пупкин, Vasiliy Pupkin";
	std::wstring cppwstr = wstr;
	/* UTF-8 */
	char *str = "Василий Пупкин Vasiliy Pupkin";
	std::string cppstr = str;
	/* In cp1251 "Василий Vasiliy" */
	char str_array[] = { (char) 194, (char) 224, (char) 241, (char) 232, (char) 235, (char) 232, (char) 233, (char) 32, 'V', 'a', 's', 'i', 'l', 'i', 'y', (char) 0 };
	std::string cppstr1251 = str_array;

        std::tuple<int,char> tuple1 (10,'x');
        auto tuple2 = std::make_tuple ("test", 3.1, 14, 'y');

        std::vector<int> vec;
        vec.push_back(1);
        vec.push_back(2);
        std::vector<int> *ptr = &vec;
        vec.resize(100000);

	std::vector<st> vec_st;
	st s;
	s.i = 1;
	vec_st.push_back(s);
	s.i = 2;
	vec_st.push_back(s);

        std::array<int, 200> ar = { 1, 2 };

        std::deque<int> deque;
        deque.assign(7, 100);

        std::list<int> list;
        list.push_back(100);
        list.push_back(200);

        std::forward_list<int> list_fw = {77, 2, 16};
        list_fw.push_front (19);
        list_fw.push_front (34);

        std::stack<int> stack;
        stack.push(1);
        stack.push(2);
        stack.push(3);
        stack.pop();

        std::queue<int> queue;
        queue.push(1);
        queue.push(2);
        queue.push(3);
        queue.pop();

        std::set<int> set;
        set.insert(1);
        set.insert(2);
        set.insert(3);
        
        std::multiset<int> multiset;
        multiset.insert(1);
        multiset.insert(1);

        std::bitset<50> bitset0;
        bitset0.reset();
        bitset0.set(2);
        bitset0.set(42);
        std::bitset<50> bitset1;
        bitset1.set();
        bitset1.set(2, 0);
        bitset1.set(42, 0);

        std::unordered_set<std::string> set_unorder;
        set_unorder.insert("yellow");
        set_unorder.insert("green");
        set_unorder.insert("blue");

        std::unordered_map<std::string,double> map_unorder = {{"milk",2.0},{"flour",1.5}, {"mineral water",2.5}, {"water",3.5}};

        std::map<int, std::string> map;
        map.insert(std::pair<int, std::string>(1, "1"));
        map.insert(std::pair<int, std::string>(3, "str 3"));
        std::multimap<int, std::string> multimap;
        multimap.insert(std::pair<int, std::string>(2, "1"));
        multimap.insert(std::pair<int, std::string>(2, "2"));

        std::shared_ptr<int> ptr_shared(new int(4));
        std::unique_ptr<int> ptr_unique(new int [2]);
        std::auto_ptr<int> ptr_auto (new int(1));

	return 0;
}
