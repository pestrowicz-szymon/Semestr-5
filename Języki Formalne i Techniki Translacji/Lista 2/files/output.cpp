#include<iostream>
#include<cstdio>


/** Maly przyklad programu
 * 
 *  // autor Maciej Gebala
 * 
 */



using namespace std;


//! Komentarz dokumentacyjny \
	   i jego 
  
int some_function(int a) {
	return a << (1 << 4);
}

/*! Nieco inny komentarz dokumentacyjny 

	// Komentarz w komentarzu		
					
					
   */
int main()
{
  /// Komentarz dokumentacyjny \
  ciag dalszy jednolinijkowego komentarza
  int i = 5;
  
  i jego ciąg dalszy\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
  i dalszy */
  cout << "Jakis program" << endl; 
  
  cout << "Poczatek komentarza 



  
  


  
  ///// Komentarz TODO: Sprawdzić jak to jest interpretowane 
  //! i jeszcze inny komentarz */
  cout << "Koniec komentarza */ "<< endl; 
  cout << "Komentarz " << endl;
  
  /*! I jeszcze jeden
					**/
  


  /** "Dokumentujemy nasz \" kod"
  
  */
  
   
  cout << "Zabawa \" 
  cout << "Komentarz 
  cout << "Pulapka \" \
           
            \
		   /** doc */\
           \\\\" << endl;
 cout << "Zabawa \" 
 printf("Zabawa \" 
}