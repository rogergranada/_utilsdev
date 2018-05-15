#! octave -qf
function matrix = buildSvd(filename)
	f_in = fopen(filename, "rt");
	#matrix(3,2);

	if( f_in == -1)
		printf("Error, could not open file '%s'\n", filename);
		matrix=[];
		return;
	endif

	exists = "false";
	col = 1;
	row = 1;
	while(!feof(f_in))
		t = fscanf(f_in, "%c,");
		if (t == ';')
			printf("Row: %d\n",row);
			row++;
			col = 1;
		endif
		if (isdigit(t))
			t_num = str2num(t);
			matrix(col,row) = t_num;
			printf("Col: %d - Value: %d\n",col, t_num);			
			col++;
		endif
	endwhile
	fclose(f_in);
endfunction
