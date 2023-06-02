# Entire Library Requirements and Tests Traceability List

## Relation between modules, classes and the requirements and tests indexing

* global requirements - 00x
* module **polynomial** - 1xy
  * 10x - class **Polynomial**
  * 11x - class **RationalFunction**
* module **special_functions** - 2xy
* module **vectors_matrices** - 3xy
  * 31x - class **Vector**
  * 32x - class **Column**
  * 33x - class **Row**
  * 34x - class **SquareMatrix**
* module **lin_solver** - 4xy
* module **poly_solver** - 5xy

## Requirements vs Tests Traceability

| **Requirement ID** | **Covered in test(s)**                                       | **Verified \[YES/NO\]** |
| :----------------- | :----------------------------------------------------------- | :---------------------- |
| REQ-FUN-000        |                                                              | NO                      |
| REQ-FUN-001        |                                                              | NO                      |
| REQ-FUN-002        |                                                              | NO                      |
| REQ-FUN-003        |                                                              | NO                      |
| REQ-INT-000        |                                                              | NO                      |
| REQ-AWM-000        |                                                              | NO                      |
| REQ-IAR-000        |                                                              | NO                      |
| REQ-IAR-001        |                                                              | NO                      |
| REQ-IAR-002        |                                                              | NO                      |
| REQ-UDR-000        |                                                              | NO                      |
| REQ-FUN-100        | TEST-T-100                                                   | YES                     |
| REQ-FUN-101        | TEST-T-103                                                   | YES                     |
| REQ-FUN-102        | TEST-T-100                                                   | YES                     |
| REQ-FUN-103        | TEST-T-100                                                   | YES                     |
| REQ-FUN-104        | TEST-T-106, TEST-T-107                                       | YES                     |
| REQ-FUN-105        | TEST-T-107                                                   | YES                     |
| REQ-FUN-106        | TEST-T-108                                                   | YES                     |
| REQ-FUN-107        | TEST-T-108                                                   | YES                     |
| REQ-FUN-108        | TEST-T-109                                                   | YES                     |
| REQ-AWM-100        | TEST-T-101, TEST-T-104                                       | YES                     |
| REQ-AWM-101        | TEST-T-102, TEST-T-105                                       | YES                     |
| REQ-AWM-102        | TEST-T-10A                                                   | YES                     |
| REQ-AWM-103        | TEST-T-10B                                                   | YES                     |
| REQ-FUN-110        | TEST-T-110                                                   | YES                     |
| REQ-FUN-111        | TEST-T-110                                                   | YES                     |
| REQ-FUN-112        | TEST-T-110                                                   | YES                     |
| REQ-AWM-110        | TEST-T-111                                                   | YES                     |
| REQ-AWM-111        | TEST-T-112                                                   | YES                     |
| REQ-AWM-112        | TEST-T-113                                                   | YES                     |
| REQ-AWM-113        | TEST-T-114                                                   | YES                     |
| REQ-FUN-200        | TEST-A-200                                                   | YES                     |
| REQ-FUN-210        | TEST-T-210                                                   | YES                     |
| REQ-FUN-220        | TEST-T-220                                                   | YES                     |
| REQ-FUN-230        | TEST-T-230                                                   | YES                     |
| REQ-FUN-240        | TEST-T-240                                                   | YES                     |
| REQ-FUN-250        | TEST-T-250                                                   | YES                     |
| REQ-FUN-260        | TEST-T-260                                                   | YES                     |
| REQ-AWM-200        | TEST-T-200                                                   | YES                     |
| REQ-AWM-201        | TEST-T-201                                                   | YES                     |
| REQ-FUN-300        | TEST-A-300                                                   | YES                     |
| REQ-FUN-301        | TEST-T-300                                                   | YES                     |
| REQ-FUN-302        | TEST-T-300                                                   | YES                     |
| REQ-FUN-303        | TEST-T-309                                                   | YES                     |
| REQ-FUN-304        | TEST-T-30A                                                   | YES                     |
| REQ-FUN-305        | TEST-T-30A                                                   | YES                     |
| REQ-FUN-306        | TEST-T-30B                                                   | YES                     |
| REQ-FUN-307        | TEST-T-30C                                                   | YES                     |
| REQ-FUN-310        | TEST-T-305                                                   | YES                     |
| REQ-FUN-320        | TEST-T-305, TEST-T-30B                                       | YES                     |
| REQ-FUN-330        | TEST-T-305, TEST-T-30B                                       | YES                     |
| REQ-FUN-340        | TEST-T-340                                                   | YES                     |
| REQ-AWM-300        | TEST-T-303, TEST-T-30D                                       | YES                     |
| REQ-AWM-301        | TEST-T-304, TEST-T-30D                                       | YES                     |
| REQ-AWM-302        | TEST-T-306, TEST-T-30E                                       | YES                     |
| REQ-AWM-303        | TEST-T-307, TEST-T-30E                                       | YES                     |
| REQ-AWM-304        | TEST-T-308, TEST-T-30E                                       | YES                     |
| REQ-AWM-305        | TEST-T-309                                                   | YES                     |
| REQ-AWM-306        | TEST-T-309                                                   | YES                     |
| REQ-AWM-307        | TEST-T-301, TEST-T-30F                                       | YES                     |
| REQ-AWM-308        | TEST-T-302, TEST-T-30F                                       | YES                     |
| REQ-AWM-340        | TEST-T-340                                                   | YES                     |
| REQ-AWM-341        | TEST-T-341                                                   | YES                     |
| REQ-AWM-342        | TEST-T-342                                                   | YES                     ||

| **Software ready for production \[YES/NO\]** | **Rationale**                 |
| :------------------------------------------: | :---------------------------- |
| NO                                           | Under development             |
