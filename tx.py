def create_case_table(cursor) -> None:
    cursor.execute("""
        DROP TABLE IF EXISTS eoir_case;
        CREATE UNLOGGED TABLE eoir_case (
            IDNCASE                     INTEGER,
            ALIEN_CITY                  TEXT,
            ALIEN_STATE                 TEXT,
            ALIEN_ZIPCODE               TEXT,
            UPDATED_ZIPCODE             TEXT,
            UPDATED_CITY                TEXT,
            NAT                         TEXT,
            LANG                        TEXT,
            CUSTODY                     TEXT,
            SITE_TYPE                   TEXT,
            E_28_DATE                   TIMESTAMP,
            ATTY_NBR                    TEXT,
            CASE_TYPE                   TEXT,
            UPDATE_SITE                 TEXT,
            LATEST_HEARING              TIMESTAMP,
            LATEST_TIME                 TIME,
            LATEST_CAL_TYPE             TEXT,
            UP_BOND_DATE                TEXT,
            UP_BOND_RSN                 TEXT,
            CORRECTIONAL_FAC            TEXT,
            RELEASE_MONTH               TEXT,
            RELEASE_YEAR                TEXT,
            INMATE_HOUSING              TEXT,
            DATE_OF_ENTRY               TIMESTAMP,
            C_ASY_TYPE                  TEXT,
            C_BIRTHDATE                 TEXT,
            C_RELEASE_DATE              TIMESTAMP,
            UPDATED_STATE               TEXT,
            ADDRESS_CHANGEDON           TIMESTAMP,
            ZBOND_MRG_FLAG              TEXT,
            GENDER                      TEXT,
            DATE_DETAINED               TIMESTAMP,
            DATE_RELEASED               TIMESTAMP,
            LPR                         TEXT,
            DETENTION_DATE              TEXT,
            DETENTION_LOCATION          TEXT,
            DCO_LOCATION                TEXT,
            DETENTION_FACILITY_TYPE     TEXT,
            CASEPRIORITY_CODE           TEXT
        );
    """)

def create_proceeding_table(cursor) -> None:
    cursor.execute("""
        DROP TABLE IF EXISTS proceeding;
        CREATE UNLOGGED TABLE proceeding (
            IDNPROCEEDING               INTEGER,  
            IDNCASE                     INTEGER,
            OSC_DATE                    TIMESTAMP,
            INPUT_DATE                  TIMESTAMP,
            BASE_CITY_CODE              TEXT,
            HEARING_LOC_CODE            TEXT,
            IJ_CODE                     TEXT,
            TRANS_IN_DATE               TIMESTAMP,
            PREV_HEARING_LOC            TEXT,
            PREV_HEARING_BASE           TEXT,
            PREV_IJ_CODE                TEXT,
            TRANS_NBR                   INTEGER,
            HEARING_DATE                TIMESTAMP,
            HEARING_TIME                TEXT,
            DEC_TYPE                    TEXT,
            DEC_CODE                    TEXT,
            DEPORTED_1                  TEXT,
            DEPORTED_2                  TEXT,
            OTHER_COMP                  TEXT,
            APPEAL_RSVD                 TEXT,
            APPEAL_NOT_FILED            TEXT,
            COMP_DATE                   TIMESTAMP,
            ABSENTIA                    TEXT,
            VENUE_CHG_GRANTED           TIMESTAMP,
            TRANSFER_TO                 TEXT,
            DATE_APPEAL_DUE_STATUS      TIMESTAMP,
            TRANSFER_STATUS             TEXT,
            CUSTODY                     TEXT,
            CASE_TYPE                   TEXT,
            NAT                         TEXT,
            LANG                        TEXT,
            SCHEDULED_HEAR_LOC          TEXT,
            CORRECTIONAL_FAC            TEXT,
            CRIM_IND                    TEXT,
            IHP                         TEXT,
            AGGRAVATE_FELON             TEXT,
            DATE_DETAINED               TIMESTAMP,
            DATE_RELEASED               TIMESTAMP
        );
    """)

def create_schedule_table(cursor) -> None:
    cursor.execute("""
        DROP TABLE IF EXISTS schedule;
        CREATE UNLOGGED TABLE schedule (
            IDNSCHEDULE             INTEGER,
            IDNPROCEEDING           INTEGER,
            IDNCASE                 INTEGER,
            OSC_DATE                TIMESTAMP,
            GENERATION              INTEGER,
            SUB_GENERATION          INTEGER,
            REC_TYPE                TEXT,
            LANG                    TEXT,
            HEARING_LOC_CODE        TEXT,
            BASE_CITY_CODE          TEXT,
            IJ_CODE                 TEXT,
            INTERPRETER_CODE        TEXT,
            INPUT_DATE              TIMESTAMP,
            INPUT_TIME              TIME,
            UPDATE_DATE             TIMESTAMP,
            UPDATE_TIME             TIME,
            ASSIGNMENT_PATH         TEXT,
            CAL_TYPE                TEXT,
            ADJ_DATE                TIMESTAMP,
            ADJ_TIME_START          TIME,
            ADJ_TIME_STOP           TIME,
            ADJ_RSN                 TEXT,
            ADJ_MEDIUM              TEXT,
            ADJ_MSG                 TEXT,
            ADJ_ELAP_DAYS           INTEGER,
            LNGSESSNID              INTEGER,
            SCHEDULE_TYPE           TEXT,
            NOTICE_CODE             TEXT,
            BLNCLOCKOVERRIDE        BOOLEAN,
            EOIRAttorneyID          TEXT
        );
    """)

def create_reps_table(cursor) -> None:
    cursor.execute("""
        DROP TABLE IF EXISTS reps;
        CREATE UNLOGGED TABLE reps (
            IDNREPSASSIGNED             INTEGER,
            IDNCASE                     INTEGER,
            STRATTYLEVEL                TEXT,
            STRATTYTYPE                 TEXT,
            PARENT_TABLE                TEXT,
            PARENT_IDN                  INTEGER,
            BASE_CITY_CODE              TEXT,
            INS_TA_DATE_ASSIGNED        TIMESTAMP,
            E_27_DATE                   TIMESTAMP,
            E_28_DATE                   TIMESTAMP,
            BLNPRIMEATTY                BOOLEAN
        );
    """)

def create_motion_table(cursor) -> None:
    cursor.execute("""
        DROP TABLE IF EXISTS motions;
        CREATE UNLOGGED TABLE motions (
            IDNMOTION               INTEGER,
            IDNPROCEEDING           INTEGER,
            IDNCASE                 INTEGER,
            OSC_DATE                TIMESTAMP,
            REC_TYPE                TEXT,
            GENERATION              TEXT,
            SUB_GENERATION          TEXT,
            UPDATE_DATE             TIMESTAMP,
            UPDATE_TIME             TIME,
            INPUT_DATE              TIMESTAMP,
            INPUT_TIME              TIME,
            REJ                     TEXT,
            BASE_CITY_CODE          TEXT,
            HEARING_LOC_CODE        TEXT,
            IJ_CODE                 TEXT,
            IJ_NAME                 TEXT,
            DEC                     TEXT,
            COMP_DATE               TIMESTAMP,
            MOTION_RECD_DATE        TIMESTAMP,
            DATMOTIONDUE            TIMESTAMP,
            WU_MSG                  TEXT,
            APPEAL_RSVD             TEXT,
            APPEAL_NOT_FILED        TEXT,
            RESP_DUE_DATE           TIMESTAMP,
            STAY_GRANT              TEXT,
            JURISDICTION            TEXT,
            DATE_APPEAL_DUE         TIMESTAMP,
            DATE_TO_BIA             TIMESTAMP,
            DECISION_RENDERED       TIMESTAMP,
            DATE_MAILED_TO_IJ       TIMESTAMP,
            DATE_RECD_FROM_BIA      TIMESTAMP,
            DATE_TO_BIA_UPDATE      INTEGER,
            STRFILINGPARTY          TEXT,
            STRFILINGMETHOD         TEXT,
            STRCERTOFSERVICECODE    TEXT,
            E_28_RECPTFLAG          BIT VARYING,
            E_28_DATE               TIMESTAMP,
            O_CLOCK_OPTION          TEXT,
            SCHEDULED_HEAR_LOC      TEXT,
            BLNDELETED              TEXT,
            strDJScenario           TEXT
        );
    """)

def create_appeal_table(cursor) -> None:
    cursor.execute("""
        DROP TABLE IF EXISTS appeal;
        CREATE UNLOGGED TABLE appeal (
            idnAppeal               INTEGER,
            idncase                 INTEGER,
            idnProceeding           INTEGER,
            strAppealCategory       TEXT,
            strAppealType           TEXT,
            datAppealFiled          TIMESTAMP,
            strFiledBy              TEXT,
            datAttorneyE27          TIMESTAMP,
            datBIADecision          TIMESTAMP,
            strBIADecision          TEXT,
            strBIADecisionType      TEXT,
            strCaseType             TEXT,
            strLang                 TEXT,
            strNat                  TEXT,
            strProceedingIHP        TEXT,
            strCustody              TEXT,
            strProbono              TEXT
        );
    """)

def create_appln_table(cursor) -> None:
    cursor.execute("""
        DROP TABLE IF EXISTS application;
        CREATE UNLOGGED TABLE application (
            IDNPROCEEDINGAPPLN      INTEGER,
            IDNPROCEEDING           INTEGER,
            IDNCASE                 INTEGER,
            APPL_CODE               TEXT,
            APPL_RECD_DATE          TIMESTAMP,
            APPL_DEC                TEXT
        );
    """)

# This is actually the lookup charges table
# def create_charges_table(cursor) -> None:
#     cursor.execute("""
#         DROP TABLE IF EXISTS charges;
#         CREATE UNLOGGED TABLE charges (
#             idnCharges              INTEGER,
#             strCode                 INTEGER,
#             strCodeString           INTEGER,
#             strCodeDescription      TEXT,
#             applicable_case_type1   TIMESTAMP,
#             applicable_case_type2   INTEGER,
#             applicable_case_type3   INTEGER,
#             criminal_flag           INTEGER,
#             aggravate_felon         TEXT,
#             DatCreatedOn            TIMESTAMP,
#             DatModifiedOn           INTEGER,
#             blnActive               INTEGER,
#         );
#     """)

def create_charges_table(cursor) -> None:
    cursor.execute("""
        DROP TABLE IF EXISTS charges;
        CREATE UNLOGGED TABLE charges (
            IDNPRCDCHG          INTEGER,
            IDNCASE             INTEGER,
            IDNPROCEEDING       INTEGER,
            CHARGE              TEXT,
            CHG_STATUS          TEXT
        );
    """)

def create_bond_table(cursor) -> None:
    cursor.execute("""
        DROP TABLE IF EXISTS bond;
        CREATE UNLOGGED TABLE bond (
            IDNASSOCBOND            INTEGER,
            IDNPROCEEDING           INTEGER,
            IDNCASE                 INTEGER,
            OSC_DATE                TIMESTAMP,
            REC_TYPE                TEXT,
            GENERATION              INTEGER,
            SUB_GENERATION          INTEGER,
            UPDATE_DATE             TEXT,
            UPDATE_TIME             TIME,
            INPUT_DATE              TIMESTAMP,
            INPUT_TIME              TIME,
            REJ                     TEXT,
            BASE_CITY_CODE          TEXT,
            BASE_CITY_NAME          TEXT,
            HEARING_LOC_CODE        TEXT,
            IJ_CODE                 TEXT,
            IJ_NAME                 TEXT,
            DEC                     TEXT,
            COMP_DATE               TIMESTAMP,
            INITIAL_BOND            TEXT,
            REL_CON                 TEXT,
            INS_TA                  TEXT,
            BOND_HEARING_TELEPHONIC TEXT,
            SEND_MSG_WU             TEXT,
            BOND_HEAR_REQ_DATE      TIMESTAMP,
            BOND_HEARING_DATE       TIMESTAMP,
            BOND_HEARING_TIME       TIME,
            ADJ1_CAL_TYPE           TEXT,
            ADJ1_DATE               TIMESTAMP,
            ADJ1_TIME               TIME,
            ADJ1_RSN                TEXT,
            ADJ1_TELEPHONIC         TEXT,
            ADJ1_MSG                TEXT,
            ADJ2_CAL_TYPE           TEXT,
            ADJ2_DATE               TIMESTAMP,
            ADJ2_TIME               TIME,
            ADJ2_RSN                TEXT,
            ADJ2_TELEPHONIC         TEXT,
            ADJ2_MSG                TEXT,
            NEW_BOND                TEXT,
            APPEAL_REVD             TEXT,
            APPEAL_NOT_FILED        TEXT,
            DATE_APPEAL_DUE         TIMESTAMP,
            E_28_DATE               TIMESTAMP,
            SCHEDULED_HEAR_LOC      TEXT,
            BOND_TYPE               TEXT,
            FILING_METHOD           TEXT,
            FILING_PARTY            TEXT,
            DECISION_DUE_DATE       TIMESTAMP
        );
    """)

def create_custody_table(cursor) -> None:
    cursor.execute("""
        DROP TABLE IF EXISTS custody;
        CREATE UNLOGGED TABLE custody (
            IDNCUSTODY      INTEGER,
            IDNCASE         INTEGER,
            CUSTODY         TEXT,
            CHARGE          TIMESTAMP,
            CHG_STATUS      TIMESTAMP
        );
    """)

def create_juvenile_table(cursor) -> None:
    cursor.execute("""
        DROP TABLE IF EXISTS juvenile;
        CREATE UNLOGGED TABLE juvenile (
            idnJuvenileHistory      INTEGER,
            idnCase                 INTEGER,
            idnProceeding           INTEGER,
            idnJuvenile             INTEGER,
            DATCREATEDON            TIMESTAMP,
            DATMODIFIEDON           TIMESTAMP
        );
    """)


def create_atty_table(cursor) -> None:
    cursor.execute("""
        DROP TABLE IF EXISTS atty;
        CREATE UNLOGGED TABLE atty (
            EOIRAttorneyID          TEXT,
            OldAttorneyID           TEXT,
            BaseCityCode            TEXT,
            blnAttorneyActive       INTEGER,
            Source_Flag             TEXT,
            datCreatedOn            TIMESTAMP,
            datModifiedOn           TIMESTAMP
        );
    """)

def create_caseid_table(cursor) -> None:
    cursor.execute("""
        DROP TABLE IF EXISTS caseid;
        CREATE UNLOGGED TABLE caseid (
            IDNCASEID       INTEGER,
            IDNCASE         INTEGER,
            CASE_ID         TEXT
        );
    """)

def create_casepriority_table(cursor) -> None:
    cursor.execute("""
        DROP TABLE IF EXISTS casepriority;
        CREATE UNLOGGED TABLE casepriority (
            idnCasePriHistory       INTEGER,
            casePriority_code       TEXT,
            idnCase                 INTEGER,
            DATCREATEDON            TIMESTAMP,
            DATMODIFIEDON           TIMESTAMP
        );
    """)

def create_rider_table(cursor) -> None:
    cursor.execute("""
        DROP TABLE IF EXISTS rider;
        CREATE UNLOGGED TABLE rider (
            idnLeadRider                INTEGER,
            idnLeadCase                 INTEGER,
            idnRiderCase                INTEGER,
            datCreatedOn                TIMESTAMP,
            datModifiedOn               TIMESTAMP,
            datSeveredOn                TIMESTAMP,
            idnLeadProceedingStart      INTEGER,
            idnLeadProceedingEnd        INTEGER,
            idnRiderProceedingStart     INTEGER,
            idnRiderProceedingEnd       INTEGER,
            blnActive                   INTEGER
        );
    """)


def create_probono_table(cursor) -> None:
    cursor.execute("""
        DROP TABLE IF EXISTS probono;
        CREATE UNLOGGED TABLE probono (
            Case_type                       TEXT,
            DEC_212C                        TEXT,
            DEC_245                         TEXT,
            NBR_OF_CHGS                     TEXT,
            Other_dec1                      TEXT,
            Other_dec2                      TEXT,
            P_EOIR42A_DEC                   TEXT,
            P_EOIR42B_DEC                   TEXT,
            VD_DEC                          TEXT,
            WD_DEC                          TEXT,
            strCorFacility                  TEXT,
            datTranscriptServedAlien        TIMESTAMP,
            strProceedingIHP                TEXT,
            strFiledby                      TEXT,
            strNat                          TEXT,
            strLang                         TEXT,
            blnOARequestedbyAlien           INTEGER,
            blnOARequestedbyINS             INTEGER,
            blnOARequestedbyAmicus          INTEGER,
            Charge_1                        TEXT,
            Charge_2                        TEXT,
            Charge_3                        TEXT,
            Charge_4                        TEXT,
            Charge_5                        TEXT,
            Charge_6                        TEXT,
            recd_212C                       TEXT,
            recd_245                        TEXT,
            VD_recd                         TEXT,
            WD_recd                         TEXT,
            P_EOIR42A_Recd                  TEXT,
            P_EOIR42B_Recd                  TEXT,
            Dec_Code                        TEXT,
            other_comp                      TEXT,
            CRIM_IND                        TEXT,
            strA1                           TEXT,
            strA2                           TEXT,
            strA3                           TEXT,
            strAlienRegion                  TEXT,
            strAlienGender                  TEXT,
            strINSStatus                    TEXT,
            strPossibility                  TEXT,
            datROPreview                    TIMESTAMP,
            blnSelectedbyCoordinator        INTEGER,
            blnSelectedbyScreener           INTEGER,
            OptionA                         INTEGER,
            DCO_Location                    TEXT,
            CaseID                          TEXT,
            Date_Of_Entry                   TIMESTAMP,
            Inmate_Housing                  TEXT,
            datmailedtoNGO                  TIMESTAMP,
            idnAppeal                       INTEGER,
            datBriefCurrentlyDueAlien       TIMESTAMP,
            idnRepl                         INTEGER,
            blnIntrpr                       INTEGER,
            strIntrprLang                   TEXT,
            ScreenerIdn                     INTEGER,
            strDCAddress1                   TEXT,
            strDCAddress2                   TEXT,
            strDCCity                       TEXT,
            strDCState                      TEXT,
            strDCZip                        TEXT,
            blnProcessed                    INTEGER,
            datCreatedOn                    TIMESTAMP,
            datModifiedOn                   TIMESTAMP,
            strCustody                      TEXT
        );
    """)


def create_fedcourts_table(cursor) -> None:
    cursor.execute("""
        DROP TABLE IF EXISTS fedcourts;
        CREATE UNLOGGED TABLE fedcourts (
            idnAppealFedCourts                      INTEGER,
            lngAppealID                             INTEGER,
            datRequestedByOIL                       TIMESTAMP,
            strFedCourtDecision                     TEXT
        );
    """)


def create_threembr_table(cursor) -> None:
    cursor.execute("""
        DROP TABLE IF EXISTS threembr;
        CREATE UNLOGGED TABLE threembr (
            idn3MemberReferral              INTEGER,
            lngAppealID                     INTEGER,
            datReferredTo3Member            TIMESTAMP,
            datRemovedFromReferral          TIMESTAMP
        );
    """)

create_tx_functions = {
        'appeal':create_appeal_table,
        'appln':create_appln_table,
        'atty':create_atty_table,
        'bond':create_bond_table,
        'case':create_case_table,
        'caseid':create_caseid_table,
        'casepriority':create_casepriority_table,
        'charges':create_charges_table,
        'custody':create_custody_table,
        'fedcourts':create_fedcourts_table,
        'juvenile':create_juvenile_table,
        'motion':create_motion_table,
        'probono':create_probono_table,
        'proceeding':create_proceeding_table,
        'reps':create_reps_table,
        'rider':create_rider_table,
        'schedule':create_schedule_table,
        'threembr':create_threembr_table
         } #[ANKI]
