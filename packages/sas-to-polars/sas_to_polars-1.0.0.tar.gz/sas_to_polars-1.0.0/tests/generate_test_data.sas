libname t_data "./test_data";

data valid_data;
    input id name $ age;
    datalines;
        1 Alice 30
        2 Bob 35
        3 Charlie 40
        ;
run;

data empty_data;
    input id name $ age;
    if 0;
    datalines;
    ;
run;

data t_data.valid_data; set valid_data; run;
data t_data.empty_data; set empty_data; run;
