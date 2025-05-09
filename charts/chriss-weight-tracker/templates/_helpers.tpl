{{/*
Expand the name of the chart.
*/}}
{{- define "chriss-weight-tracker.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "chriss-weight-tracker.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "chriss-weight-tracker.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "chriss-weight-tracker.labels" -}}
helm.sh/chart: {{ include "chriss-weight-tracker.chart" . }}
{{ include "chriss-weight-tracker.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "chriss-weight-tracker.selectorLabels" -}}
app.kubernetes.io/name: {{ include "chriss-weight-tracker.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}


{{/*
Pod spec
*/}}
{{- define "chriss-weight-tracker.podSpec" -}}
{{- with .Values.imagePullSecrets }}
imagePullSecrets:
  {{- toYaml . | nindent 2 }}
{{- end }}
containers:
  - name: '{{ include "chriss-weight-tracker.fullname" . }}-scheduled-job'
    image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
    imagePullPolicy: "{{ .Values.image.pullPolicy }}"
    securityContext:
      {{- toYaml .Values.securityContext | nindent 6 }}
    args:
      - "--google-sheet"
      - "{{ .Values.googleSheetUrl }}"
      - "--server"
      - "{{ .Values.service.port }}"
    env:
      - name: FITBIT_DATABASE
        value: "/data/db/fitbit.sqlite"
      - name: FITBIT_REDIRECT_URI
        value: https://{{ .Values.ingress.hostname }}/
      - name: FITBIT_CLIENT_ID
        valueFrom:
          secretKeyRef:
            name: "{{ .Values.fitbitSecretName }}"
            key: FITBIT_CLIENT_ID
      - name: FITBIT_CLIENT_SECRET
        valueFrom:
          secretKeyRef:
            name: "{{ .Values.fitbitSecretName }}"
            key: FITBIT_CLIENT_SECRET
      - name: GOOGLE_SERVICE_ACCOUNT
        value: "/data/google-service-account/service-account.json"
      - name: HEIGHT
        value: "{{ .Values.height }}"
    volumeMounts:
      - mountPath: /data/google-service-account
        name: google-service-account
      - mountPath: /data/db
        name: db
    resources:
      {{- toYaml .Values.resources | nindent 6 }}
volumes:
  - name: google-service-account
    secret:
      secretName: "{{ .Values.googleServiceAccountSecretName }}"
  - name: db
    persistentVolumeClaim:
      claimName: '{{ include "chriss-weight-tracker.fullname" . }}-db'
restartPolicy: Never
{{- with .Values.nodeSelector }}
nodeSelector:
  {{- toYaml . | nindent 2 }}
{{- end }}
{{- with .Values.affinity }}
affinity:
  {{- toYaml . | nindent 2 }}
{{- end }}
{{- with .Values.tolerations }}
tolerations:
  {{- toYaml . | nindent 2 }}
{{- end }}
{{- end }}
