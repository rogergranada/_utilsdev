#!/usr/bin/perl -w

use strict;
use Spreadsheet::ParseExcel;
use Spreadsheet::WriteExcel;

my $fileoutput = $ARGV[0];
my $fileinput_old = $ARGV[1];
my $fileinput_new = $ARGV[2];
my $fileinput_ev1 = $ARGV[3];
my $fileinput_ev2 = $ARGV[4];
my $fileinput_ev3 = $ARGV[5];
my $thesaurus = $ARGV[6];

my $parser_old = Spreadsheet::ParseExcel->new();
my $parser_new = Spreadsheet::ParseExcel->new();
my $workbook_old = $parser_old->parse($fileinput_old);
my $workbook_new = $parser_new->parse($fileinput_new);
my $workbook_out = Spreadsheet::WriteExcel->new($fileoutput);

if ( !defined $workbook_old || !defined $workbook_new) {
    die $parser_old->error(), ".\n"; #$parser_new <anche>
}

for my $worksheet_old ( $workbook_old->worksheets() ) {
	my $label = $worksheet_old->get_name();
	my $worksheet_new = $workbook_new->worksheet($label);
	my $worksheet_out = $workbook_out->add_worksheet($label);

	$worksheet_out->write(0, 0, "Mutual Information");	
	$worksheet_out->write(0, 1, "19/4 TurneyS3");
	$worksheet_out->write(0, 2, "14/6 TurneyS3");
	$worksheet_out->write(0, 3, "Evaluator 1");
	$worksheet_out->write(0, 4, "Evaluator 2");
	$worksheet_out->write(0, 5, "Evaluator 3");

	for my $row ( 1 .. 10 ) {
		my $cell_im = $worksheet_new->get_cell( $row, "9" );
		my $cell_old = $worksheet_old->get_cell( $row, "1" );
		my $cell_new = $worksheet_new->get_cell( $row, "1" );
		
		$worksheet_out->write($row, 0, $cell_im->value());
		$worksheet_out->write($row, 1, $cell_old->value());
		$worksheet_out->write($row, 2, $cell_new->value());
	}

	open (my $filereaderEv1, "<", $fileinput_ev1) or die "Cannot open file $fileinput_ev1:$!";
	my $rowEv1 = 1;
	my $seed_ev1;
	while(<$filereaderEv1>){
		chop($_);
		my $line = $_;
		
		if ($line =~ /Seed: /){		
			$seed_ev1 = (split("Seed: ",$line))[1];
		}

		if ($line =~ /] </){
			my $similarity = (split("= ",$line))[1];
			my $thesauri = (split("> ",(split("\] <",$line))[1]))[0];
			my $term = (split(" =",(split ("> ",$line))[1]))[0];

#print "SEED: ".$seed." - LABEL: ".$label."\n";
			if ($thesauri =~ /$thesaurus/ && $similarity =~ /^[Ss]imilar/ && $seed_ev1 eq $label){
				$worksheet_out->write($rowEv1, 3, $term);
				$rowEv1++;
			}
		}
	}
	close ($fileinput_ev1);

	open (my $filereaderEv2, "<", $fileinput_ev2) or die "Cannot open file $fileinput_ev2:$!";
	my $rowEv2 = 1;
	my $seed_ev2;
	while(<$filereaderEv2>){
		chop($_);
		my $line = $_;
		
		if ($line =~ /Seed: /){		
			$seed_ev2 = (split("Seed: ",$line))[1];
		}

		if ($line =~ /] </){
			my $similarity = (split("= ",$line))[1];
			my $thesauri = (split("> ",(split("\] <",$line))[1]))[0];
			my $term = (split(" =",(split ("> ",$line))[1]))[0];

#print "SEED: ".$seed." - LABEL: ".$label."\n";
			if ($thesauri =~ /$thesaurus/ && $similarity =~ /^[Ss]imilar/ && $seed_ev2 eq $label){
				$worksheet_out->write($rowEv2, 4, $term);
				$rowEv2++;
			}
		}
	}
	close ($fileinput_ev2);

	open (my $filereaderEv3, "<", $fileinput_ev3) or die "Cannot open file $fileinput_ev3:$!";
	my $rowEv3 = 1;
	my $seed_ev3;
	while(<$filereaderEv3>){
		chop($_);
		my $line = $_;
		
		if ($line =~ /Seed: /){		
			$seed_ev3 = (split("Seed: ",$line))[1];
		}

		if ($line =~ /] </){
			my $similarity = (split("= ",$line))[1];
			my $thesauri = (split("> ",(split("\] <",$line))[1]))[0];
			my $term = (split(" =",(split ("> ",$line))[1]))[0];

#print "SEED: ".$seed." - LABEL: ".$label."\n";
			if ($thesauri =~ /$thesaurus/ && $similarity =~ /^[Ss]imilar/ && $seed_ev3 eq $label){
				$worksheet_out->write($rowEv3, 5, $term);
				$rowEv3++;
			}
		}
	}
	close ($fileinput_ev3);
}
