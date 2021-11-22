import java.util.*;
class SudokuSolver {
	public static int checkSquare(int [][] s, int x,int y,int num) {
		int i = 0;
 		int j = 0;
		if (x<3)
			i=0;
		else if (x<6)
			i=3;
		else
			i=6;	
		if (y<3)
			j=0;
		else if (y<6)
			j=3;
		else
			j=6;
		for (int ti = i; ti<i+3; ti++) {
			for (int tj = j; tj<j+3; tj++) {
				if (s[ti][tj]==num)
					return 1;
			}
		}
		return 0;	
	}
	public static int checkRow(int [][] s, int x,int y,int num) {
		for (int i = 0; i<9; i++) {
			if (s[x][i] == num) {
				return 1;
			}
		}
		return 0;
	}
	public static int checkColumn(int [][] s, int x,int y,int num) {
		for (int i = 0; i<9; i++) {
			if (s[i][y] == num) {
				return 1;
			}
		}
		return 0;
	}

	public static void display(int[][] s) {
		for (int i = 0; i<9; i++) {
			for (int j = 0; j<9; j++) {
				System.out.print(s[i][j] + " ");
			}
			System.out.println();
		}
	}
	public static int solve(int[][] s, int x, int y) {
		int num=1;
		if (s[x][y]!=0) {
			if (x==8 && y==8) {
				return 1;
			}
			if (x<8) {
				x=x+1;
			}
			else {
				x=0;
				y=y+1;
			}	
			if (solve(s,x,y)==1) {
				return 1;
			}
			else {
				return 0;
			}
		}				
		if (s[x][y]==0) { 
			while(num<10) {
				int tx = 0;
				int ty = 0;
				if 	(checkColumn(s,x,y,num)==0 && checkRow(s,x,y,num)==0 && checkSquare(s,x,y,num)==0) {
					s[x][y]=num;
					if (x==8 && y==8) {
						return 1;
					}
					if (x<8) {
						tx=x+1;
						ty=y;
					}	
					else {
						tx=0;
						ty=y+1;
					}		
					if (solve(s,tx,ty)==1) {
						return 1;
					}
				}	
				num=num+1;
			}		
			s[x][y]=0;
			return 0;
		}	
    return 0;		
	}
	public static void main(String args[]) {
		int[][] sudoku = new int[][] { 
            {0, 0, 0, 8, 0, 0, 0, 0, 0}, 
            {4, 0, 0, 0, 1, 5, 0, 3, 0}, 
            {0, 2, 9, 0, 4, 0, 5, 1, 8}, 
            {0, 4, 0, 0, 0, 0, 1, 2, 0}, 
            {0, 0, 0, 6, 0, 2, 0, 0, 0}, 
            {0, 3, 2, 0, 0, 0, 0, 9, 0}, 
            {6, 9, 3, 0, 5, 0, 8, 7, 0}, 
            {0, 5, 0, 4, 8, 0, 0, 0, 1}, 
            {0, 0, 0, 0, 0, 3, 0, 0, 0} 
    	};
    	if (solve(sudoku,0,0)==1) {
        System.out.println("Solution Found:\n");
    		display(sudoku);
    	}
    	else {
    		System.out.println("No Solution Found.");
    	}
	}
}