#include <iostream>
#include <cstdlib>
#include <fstream>
#include <sstream>

#define FIRST_ARG 1
#define LAST_ARG 2
#define CHROME_DRIVER_PATH 3

using namespace std;

string execute(const string&);

//echo $(kubectl -n bluexolo get svc nginx -o jsonpath='{.status.loadBalancer.ingress[0].ip}')

int main(int argc, char * argv[]) {
    if(argc>1)
    {
        _putenv_s("CHROMEDRIVER_EXECUTABLE_PATH",argv[CHROME_DRIVER_PATH]);
        _putenv_s("BX_LOGIN_TEST_EMAIL",argv[FIRST_ARG]);
        _putenv_s("BX_LOGIN_TEST_PASSWORD",argv[LAST_ARG]);
        string ip(execute("kubectl -n bluexolo get svc nginx -o jsonpath='{.status.loadBalancer.ingress[0].ip}'"));
        ip.erase(0,1);
        ip.pop_back();
        stringstream ss;
        ss << "BX_LOGIN_URL=http://"<<ip<<":80/login/";
        cout<<ss.str()<<endl;
        putenv(ss.str().c_str());
        cout<<ss.str();
        system("python loginTest.py");
    }
    else
    {
        cout<<"No params were provided"<<endl;
    }
    return 0;
}

std::string execute(const std::string& command) {
    system((command + " > temp.txt").c_str());
 
    std::ifstream ifs("temp.txt");
    std::string ret{ std::istreambuf_iterator<char>(ifs), std::istreambuf_iterator<char>() };
    ifs.close();
    if (std::remove("temp.txt") != 0) {
        perror("Error deleting temporary file");
    }
    return ret;
}