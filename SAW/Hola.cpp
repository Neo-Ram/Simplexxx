#include<iostream>

using namespace std;

int main(){
	
	int a, b, r;
	
	cout<<"Ingrese un numero: "<<endl;
	cin>>a;
	cout<<"Ingrese otro numero: "<<endl;
	cin>>b;
	cout<<"------------------------------------"<<endl;
	r = a + b;
	cout<<"El resultado de la suma: " << r << endl;
	cout<<"El resultado de la resta es: " << a-b << endl;
	cout<<"El resultado de la division es: " << a/b << endl;
	cout<<"El resultado de la multiplicacion es: " << a*b;
	
	return 0;
}