class acronymRepository:
    def __init__(self, env):
        self.env = env
        
        
    def get_acronym_per_comparison(self, acronym1 , acronym2):
        sql = """
            SELECT DISTINCT aux_gorsdav.*
            FROM SCBCRSE
            INNER JOIN 
            (SELECT SCBCRSE_SUBJ_CODE||SCBCRSE_CRSE_NUMB SUBJ, MAX(SCBCRSE_EFF_TERM) TERM
            FROM SCBCRSE
            GROUP BY SCBCRSE_SUBJ_CODE||SCBCRSE_CRSE_NUMB
            ) AX_CRSE ON SCBCRSE_SUBJ_CODE||SCBCRSE_CRSE_NUMB = AX_CRSE.SUBJ
            AND SCBCRSE_EFF_TERM = AX_CRSE.TERM
            INNER JOIN (
            SELECT SMRACAA_RULE REGLA
            FROM SMRACAA 
            INNER JOIN (
            SELECT SMRACAA_AREA AREA, MAX(SMRACAA_TERM_CODE_EFF) TERM
            FROM SMRACAA
            GROUP BY SMRACAA_AREA
            ) REGLA ON REGLA.AREA=SMRACAA_AREA
            AND REGLA.TERM=SMRACAA_TERM_CODE_EFF
            ) AX_REGLA ON AX_REGLA.REGLA=SCBCRSE_SUBJ_CODE||SCBCRSE_CRSE_NUMB
            INNER JOIN (
            SELECT * FROM
            (
            SELECT SUBSTR(GORSDAV_PK_PARENTTAB,1,4)||SUBSTR(GORSDAV_PK_PARENTTAB,6,4) SUBJ,SUBSTR(GORSDAV_PK_PARENTTAB,11,6) TERM,
            GORSDAV_ATTR_NAME ATTR, GORSDAV_VALUE VALUE
            FROM GORSDAV 
            WHERE GORSDAV_TABLE_NAME='SCBCRSE'
            )
            PIVOT (
            MAX(SYS.ANYDATA.accessVarchar2(VALUE))
            FOR ATTR IN (
            'HORAS_DOCENCIA' AS HORAS_DOCENCIA,
            'HORAS_DOCENCIA_PRESENCIAL_H' AS HORAS_DOCENCIA_PRESENCIAL_H,
            'HORAS_DOCENCIA_VIRTUAL_H' AS HORAS_DOCENCIA_VIRTUAL_H,
            'HORAS_DOCENCIA_O' AS HORAS_DOCENCIA_O,
            'HORAS_LABORATORIO_DOCENCIA' AS HORAS_LABORATORIO_DOCENCIA,
            'HORAS_LABORATORIO_DOCENCIA_H' AS HORAS_LABORATORIO_DOCENCIA_H,
            'HORAS_EXTERNADO_DOCENCIA' AS HORAS_EXTERNADO_DOCENCIA,
            'HORAS_EXTERNADO_DOCENCIA_H' AS HORAS_EXTERNADO_DOCENCIA_H,
            'HORAS_APLICACION' AS HORAS_APLICACION,
            'HORAS_APLICACION_H' AS HORAS_APLICACION_H,
            'HORAS_APLICACION_O' AS HORAS_APLICACION_O,
            'HORAS_APLICACION_LABORATORIO' AS HORAS_APLICACION_LABORATORIO,
            'HORAS_APLICACION_LAB_H' AS HORAS_APLICACION_LAB_H,
            'HORAS_APLICACION_LAB_O' AS HORAS_APLICACION_LAB_O,
            'HORAS_PRACT_PREPROFESIONALES' AS HORAS_PRACT_PREPROFESIONALES,
            'HORAS_PRACT_PREPROF_H' AS HORAS_PRACT_PREPROF_H,
            'HORAS_PRACT_PREPROF_O' AS HORAS_PRACT_PREPROF_O,
            'HORAS_SERVICIO_COMUNIDAD' AS HORAS_SERVICIO_COMUNIDAD,
            'HORAS_SERVICIO_COMUNIDAD_H' AS HORAS_SERVICIO_COMUNIDAD_H,
            'HORAS_SERVICIO_COMUNIDAD_O' AS HORAS_SERVICIO_COMUNIDAD_O,
            'TOTAL_HORAS_AUTONOMAS' AS TOTAL_HORAS_AUTONOMAS,
            'TOTAL_HORAS_AUTONOMAS_H' AS TOTAL_HORAS_AUTONOMAS_H,
            'TOTAL_HORAS_AUTONOMAS_O' AS TOTAL_HORAS_AUTONOMAS_O,
            'HORAS_TITULACION' AS HORAS_TITULACION,
            'HORAS_TITULACION_H' AS HORAS_TITULACION_H,
            'HORAS_TITULACION_O' AS HORAS_TITULACION_O,
            'SESIONES_DOCENCIA' AS SESIONES_DOCENCIA,
            'SESIONES_LABORATORIO' AS SESIONES_LABORATORIO,
            'SESIONES_EXTERNADO' AS SESIONES_EXTERNADO,
            'SESIONES_O' AS SESIONES_O,
            'SEMANAS_EXTERNADO' AS SEMANAS_EXTERNADO,
            'SEMANAS_LABORATORIO' AS SEMANAS_LABORATORIO,
            'HORAS_ADICIONALES_SILABO' AS HORAS_ADICIONALES_SILABO
            ))) AUX_GORSDAV ON AUX_GORSDAV.SUBJ=SCBCRSE_SUBJ_CODE||SCBCRSE_CRSE_NUMB
            AND AUX_GORSDAV.TERM=SCBCRSE_EFF_TERM
            AND AUX_GORSDAV.SUBJ IN (:acronym1, :acronym2)
            """       
        dbsource=self.env['base.external.dbsource'].search([('enabled','=',True)])
        if not dbsource:
            return False
        res = dbsource.execute(sql, {'acronym1': acronym1, 'acronym2':acronym2})
        return res if res else False