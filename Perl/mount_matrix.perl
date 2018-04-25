#!/usr/bin/perl -w

$file_output_An = $ARGV[0]; # Output file
$file_output_aN = $ARGV[1]; # Output file
#$file_output_Sv = $ARGV[2]; # Output file
#$file_output_sV = $ARGV[3]; # Output file
#$file_output_Vo = $ARGV[4]; # Output file
#$file_output_vO = $ARGV[5]; # Output file
$file_output_an = $ARGV[6]; # Output file
#$file_output_sv = $ARGV[7]; # Output file
#$file_output_vo = $ARGV[8]; # Output file
$file_relations = $ARGV[9]; # Input file

open (my $filereaderInput, "<$file_relations") or die "Cannot open file $file_relations:$!";
open (my $filewriterAn, ">$file_output_An") or die "Cannot open file $file_output_An:$!";
open (my $filewriteraN, ">$file_output_aN") or die "Cannot open file $file_output_aN:$!";
#open (my $filewriterSv, ">$file_output_Sv") or die "Cannot open file $file_output_Sv:$!";
#open (my $filewritersV, ">$file_output_sV") or die "Cannot open file $file_output_sV:$!";
#open (my $filewriterVo, ">$file_output_Vo") or die "Cannot open file $file_output_Vo:$!";
#open (my $filewritervO, ">$file_output_vO") or die "Cannot open file $file_output_vO:$!";
open (my $filewriteran, ">$file_output_an") or die "Cannot open file $file_output_an:$!";
#open (my $filewritersv, ">$file_output_sv") or die "Cannot open file $file_output_sv:$!";
#open (my $filewritervo, ">$file_output_vo") or die "Cannot open file $file_output_vo:$!";

%hash_relations = ();
%hash_An = ();
%hash_An_index = ();
%hash_aN = ();
%hash_aN_index = ();
#%hash_Sv = ();
#%hash_Sv_index = ();
#%hash_sV = ();
#%hash_sV_index = ();
#%hash_Vo = ();
#%hash_Vo_index = ();
#%hash_vO = ();
#%hash_vO_index = ();
$index_An = 0;
$index_aN = 0;
#$index_Sv = 0;
#$index_sV = 0;
#$index_Vo = 0;
#$index_vO = 0;
while(<$filereaderInput>){
	chop($_);
	$line = $_;

	@splited_line = split("#",$line);
	$relation = &trim(lc($splited_line[0]));
	$modifier = &trim(lc($splited_line[1]));
	$noun = &trim(lc($splited_line[2]));
	$frequency = $splited_line[3];
#print $line."##\n";
#####################################################################################################
# This program mount a matrix "noun x relation" where the number of the relation is the frequency.  #
# It's mounted three matrices: An x aN, Sv x sV and Vo x vO, explained as followed:                 #
#   An x aN = Noun and its modifiers (using: nn, amod, of)                                          #
#   Sv x sV = Verbs when they have subjects (using: subj, agent)                                    #
#   Vo x vO = Verbs when they have objects (using: _obj, iobj)                                      #
# These matrices are built as:                                                                      #
#   An/aN = Adjective ($modifier) x Noun ($noun)                                                    # 
#   Sv/sV = Subject ($noun) x Verb ($modifier)                                                      #
#   Vo/vO = Verb ($modifier) x Object ($noun)                                                       #
#####################################################################################################

	if ($relation =~ /of|nn|amod/ && $modifier !~ /^$|^\d+$/ && $noun !~ /^\d+$/){
		$relation = "an";
		if (!exists $hash_An{$modifier}){
			$hash_An{$modifier} = $index_An;
			$hash_An_index{$index_An} = $modifier;
			$index_An++;
		}
		if (!exists $hash_aN{$noun}){
			$hash_aN{$noun} = $index_aN;
			$hash_aN_index{$index_aN} = $noun;
			$index_aN++;
		}

		if (exists $hash_relations{$relation."#".$modifier."#".$noun}){
			$hash_relations{$relation."#".$modifier."#".$noun}+= $frequency;
		}else{
			$hash_relations{$relation."#".$modifier."#".$noun} = $frequency;
		}
#	}elsif ($relation =~ /_subj|agent/ && $modifier !~ /^$|^\d+$/ && $noun !~ /^\d+$/){
#		$relation = "sv";
#		if (!exists $hash_Sv{$noun}){
#			$hash_Sv{$noun} = $index_Sv;
#			$hash_Sv_index{$index_Sv} = $noun;
#			$index_Sv++;
#		}
#		if (!exists $hash_sV{$modifier}){
#			$hash_sV{$modifier} = $index_sV;
#			$hash_sV_index{$index_sV} = $modifier;
#			$index_sV++;
#		}
#	}elsif ($relation =~ /_obj|iobj/ && $modifier !~ /^$|^\d+$/ && $noun !~ /^\d+$/){
#		$relation = "vo";
#		if (!exists $hash_Vo{$modifier}){
#			$hash_Vo{$modifier} = $index_Vo;
#			$hash_Vo_index{$index_Vo} = $modifier;
#			$index_Vo++;
#		}
#		if (!exists $hash_vO{$noun}){
#			$hash_vO{$noun} = $index_vO;
#			$hash_vO_index{$index_vO} = $noun;
#			$index_vO++;
#		}
	}
#	if (exists $hash_relations{$relation."#".$modifier."#".$noun}){
#		$hash_relations{$relation."#".$modifier."#".$noun}+= $frequency;
#	}else{
#		$hash_relations{$relation."#".$modifier."#".$noun} = $frequency;
#	}
}

foreach my $value (sort {$a cmp $b} keys %hash_An_index) {
  print $filewriterAn $value." : ".$hash_An_index{$value}."\n";
}
foreach my $value (sort {$a cmp $b} keys %hash_aN_index) {
  print $filewriteraN $value." : ".$hash_aN_index{$value}."\n";
}
#foreach my $value (sort {$a cmp $b} keys %hash_Sv_index) {
#  print $filewriterSv $value." : ".$hash_Sv_index{$value}."\n";
#}
#foreach my $value (sort {$a cmp $b} keys %hash_sV_index) {
#  print $filewritersV $value." : ".$hash_sV_index{$value}."\n";
#}
#foreach my $value (sort {$a cmp $b} keys %hash_Vo_index) {
#  print $filewriterVo $value." : ".$hash_Vo_index{$value}."\n";
#}
#foreach my $value (sort {$a cmp $b} keys %hash_vO_index) {
#  print $filewritervO $value." : ".$hash_vO_index{$value}."\n";
#}

############################################################################################################################################################
#
# Build the matrix aN x An where: aN -> $i and An -> $j
#
############################################################################################################################################################

$size_hash_An = keys %hash_An_index;
$size_hash_aN = keys %hash_aN_index;
#print "An: ".$size_hash_An." -> aN: ".$size_hash_aN."\n";
#print $filewriteran "# Created by Octave 3.0.1, Fri Oct 22 16:01:53 2010 BRT <roger\@roger>\n# name: a\n# type: matrix\n# rows: $size_hash_aN\n# columns: $size_hash_An\n";
for ($i=0; $i<=$size_hash_aN-1; $i++){
	#print $filewriteran " ";
	for ($j=0; $j<=$size_hash_An-1; $j++){
		if (exists $hash_relations{"an#".$hash_An_index{$j}."#".$hash_aN_index{$i}}){
			print $filewriteran $hash_relations{"an#".$hash_An_index{$j}."#".$hash_aN_index{$i}};
#			print $filewriterAn "an#".$hash_An_index{$i}."#".$hash_aN_index{$j}." :: ".$hash_relations{"an#".$hash_An_index{$i}."#".$hash_aN_index{$j}}."\n";
		}else{
			print $filewriteran "0";
		}
		if ($j < $size_hash_An-1){
			print $filewriteran " ";
		}
	}
	if ($i < $size_hash_aN-1){
		print $filewriteran ";";
	}
}
print $filewriteran "";
#print $filewriteran $string_out_an."\n";

############################################################################################################################################################
#
# Build the matrix sV x Sv where: sV -> $i and Sv -> $j
#
############################################################################################################################################################

#$size_hash_Sv = keys %hash_Sv_index;
#$size_hash_sV = keys %hash_sV_index;
#$string_out_sv = "[";
#for ($i=0; $i<=$size_hash_sV-1; $i++){
#	for ($j=0; $j<=$size_hash_Sv-1; $j++){
#		if (exists $hash_relations{"sv#".$hash_sV_index{$i}."#".$hash_Sv_index{$j}}){
#			$string_out_sv .= $hash_relations{"sv#".$hash_sV_index{$i}."#".$hash_Sv_index{$j}};
#		}else{
#			$string_out_sv .= "0";
#		}
#		if ($j < $size_hash_Sv-1){
#			$string_out_sv .= ", ";
#		}
#	}
#	if ($i < $size_hash_sV-1){
#		$string_out_sv .= "; ";
#	}
#}
#$string_out_sv .= "]";
#print $filewritersv $string_out_sv."\n";

############################################################################################################################################################
#
# Build the matrix vO x Vo where: vO -> $i and Vo -> $j
#
############################################################################################################################################################

#$size_hash_Vo = keys %hash_Vo_index;
#$size_hash_vO = keys %hash_vO_index;
#$string_out_vo = "[";
#for ($i=0; $i<=$size_hash_Vo-1; $i++){
#	for ($j=0; $j<=$size_hash_vO-1; $j++){
#		if (exists $hash_relations{"vo#".$hash_Vo_index{$i}."#".$hash_vO_index{$j}}){
#			$string_out_vo .= $hash_relations{"vo#".$hash_Vo_index{$i}."#".$hash_vO_index{$j}};
#		}else{
#			$string_out_vo .= "0";
#		}
#		if ($j < $size_hash_vO-1){
#			$string_out_vo .= ", ";
#		}
#	}
#	if ($i < $size_hash_Vo-1){
#		$string_out_vo .= "; ";
#	}
#}
#$string_out_vo .= "]";
#print $filewritervo $string_out_vo."\n";

############################################################################################################################################################
#
# Subfunctions used in this program
#
############################################################################################################################################################

sub trim($){
	my $string = shift;
	$string =~ s/^\s+//;
	$string =~ s/\s+$//;
	return $string;
}
