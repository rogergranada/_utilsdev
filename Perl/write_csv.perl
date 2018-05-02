#!/usr/bin/perl -w

use strict;
use Spreadsheet::WriteExcel;

my $workbook  = Spreadsheet::WriteExcel->new('test.xls');
my $worksheet = $workbook->add_worksheet();
$worksheet->write(0, 0, "Hi Excel!");
