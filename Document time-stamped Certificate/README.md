## Document time-stamped certificate
This application relates to securely time-stamping a document that one may have prepared some moments ago.

### Functions
- Documnet uploading
- GMT date & time-stamping server
- Time-stamp documents (in some standard format) with the current GMT data/time and a digital signature.
- Download time-stamped documents
- Should be possible to establish the fact that the document existed at the date/time stamped, and that the document has not been modified.

### Questions
1. How and where do you get the correct GMT date and time? And when is the correct GMT date/time obtained?
2. Is the source reliable? Is the GMT date and time obtained in a secure manner?
3. How do you ensure privacy, in that the server does not see/keep the original document?
4. How do you share the document with others in a secure manner with the GMT date/time preserved, and its integrity un-disturbed?
5. How does one ensure that the user (both the owner and anyone verifying the date/time) uses the correct “public-key” of the server stamping/signing the “GMT date/time”.
