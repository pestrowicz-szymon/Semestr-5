#include<iostream>
#include<cstdio>


/** Maly przyklad programu
 * 
 *  // autor Maciej Gebala
 * 
 */


// /*
using namespace std;
// */ 

//! Komentarz dokumentacyjny
	   //i jego // ciag dalszy
  /* i dalszy */
int some_function(int a) {
	return a << (1 << 4);
}

/*! Nieco inny komentarz dokumentacyjny 

	// Komentarz w komentarzu		
					
					
   */
int main()
{
  /// Komentarz dokumentacyjny
  int i = 5;
  // Komentarz jednolinijkowy
  cout << "Jakis program" << endl; // ;
  // A tutaj taki komentarz \ 
  cout << "Poczatek komentarza /*" << endl; // ala // <- gcc to potraktuje jako komentarz
  /*
	Taki sobie komentarz
	/** z komentarzem w srodku */
  
  /*
	/// Komentarz nie-dokumentacyjny
  */
  // /// Komentarz /** rozne rzeczy /
  ///// Komentarz TODO: Sprawdzić jak to jest interpretowane 
  //! i jeszcze inny komentarz */
  cout << "Koniec komentarza */ "<< endl; // kot
  cout << "Komentarz /* ala */" << endl;
  
  /*! I jeszcze jeden
					**/
  /* komentarz "taki z c\"zyms w cudzyslowie""""""""""""""""
  /*
  */
  /** "Dokumentujemy nasz \" kod"
  
  */
  // nie moze byc "za latwo", a co!
   // i jeszcze jeden */
  cout << "Zabawa \" // \\\\\"ala i kot \\\\" << endl; // abcabcabc "
  cout << "Komentarz // kot " << endl;
  cout << "Pulapka \" \
           // ma \
           /* \\\"ma\" */ \
		   /** doc */\
           \\\\" << endl;
 cout << /*Proba*/"Zabawa \" // ala i kot " << endl;	   
 printf("Zabawa \" // ala i kot ");
}