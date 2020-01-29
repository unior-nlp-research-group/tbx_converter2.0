# TBX-Basic Download Package

This download package will be updated regularly.

Last update: June 12, 2018.

## Recent changes:

* June 12, 2018 - Updated to include change in TBX-Basic:
    * *REPLACED* /crossReference/ is not /relatedConcept/ and /relatedTerm/
* November 27, 2017 - Updated the package to conform to newest draft of ISO 30042:
    * *REMOVED (obsolete)* TBXBasiccoreStructureV02.dtd
    * *REMOVED (obsolete)* TBX-Basic specification
    * *REMOVED (obsolete)* TBX-Basic eXtensible Constraints Specification file
    * *REMOVED (obsolete)* DTD for validating the XCS file
    * *REPLACED* Integrated RNG Schema for TBX-Basic TBXBasicRNGV02.rng -> TBXcoreStructV03_TBX-Basic_integrated.rng
    * *UPDATED* TBX-Basic sample files
* April 30, 2013 - Updated demo files to point to local copy of TBXBasicXCSV02.xcs
* February 26, 2009 - Updated this readme file with a new date and the two changes listed below:
* January 26, 2009 - updated the RNG schema to allow a context sentence to occur in a descripGrp
* January 23, 2009 - added a context source data category to the specification document and samples

## Contents
This package contains the following files:

1. The Integrated RNG Schema for TBX-Basic - TBXcoreStructV03_TBX-Basic_integrated.rng
2. TBX-Basic SCH Schema - TBX-Basic_DCA.sch
2. TBX-Basic sample files - all files ending with the "tbx" extension
3. tbxcheck-1.2.9.jar- Tool for checking TBX files for errors (requires Java)
4. TBXStarterGuide.docx- Tutorial to help users learn how to use TBX and the TBX Checker and other TBX-validating tools
    * **The Starter Guide is being rewritten to accurately describe the 2018 version of TBX-Basic.**

The TBX Checker is a validating parser specifically designed for TBX files. **Note that the checker can only be used to check 2008 TBX-Basic files until it is either updated or replaced.**
It is available from the following Web site.

http://sourceforge.net/projects/tbxutil/

As an alternative to using the TBX Checker to validate TBX-Basic files, you can use
the Integrated RNG Schema and any off-the-shelf XML validator that supports the RelaxNG
and Schematron languages, such as oXygen.
