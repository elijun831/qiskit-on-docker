{{- define "qiskit-monitoring.serviceAccountName" -}}
{{- if .Values.serviceAccount.name -}}
{{ .Values.serviceAccount.name }}
{{- else -}}
{{ include "qiskit-monitoring.fullname" . }}
{{- end -}}
{{- end -}}

{{- define "qiskit-monitoring.labels" -}}
helm.sh/chart: {{ include "qiskit-monitoring.chart" . }}
app.kubernetes.io/name: {{ include "qiskit-monitoring.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Chart.AppVersion }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end -}}

{{- define "qiskit-monitoring.chart" -}}
{{ .Chart.Name }}-{{ .Chart.Version }}
{{- end -}}

{{- define "qiskit-monitoring.name" -}}
{{ .Chart.Name }}
{{- end -}}

{{- define "qiskit-monitoring.fullname" -}}
{{ .Release.Name }}-{{ .Chart.Name }}
{{- end -}}
