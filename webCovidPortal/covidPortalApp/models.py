from __future__ import absolute_import

from django.db import models
from django.contrib.auth.models import User

class UploadFolder(models.Model):
    name = models.CharField(max_length=256)
    fileName = models.CharField(max_length=512, blank = True, null = True)
    fileType = models.CharField(max_length=256, blank = True, null = True)
    user = models.ForeignKey(User, blank = True, null=True, on_delete=models.CASCADE)
    chksum = models.CharField(max_length=256, default='')
    description = models.CharField(max_length=512, blank = True, null = True)
    status = models.CharField(max_length=255, blank = True, null = True)
    uploadedDate = models.DateTimeField(max_length=255, blank = True, null = True)
    analysisProtocol = models.CharField(max_length=255, blank = True, null = True)
    analysisSubmittedDate = models.DateTimeField(max_length=255, blank = True, null = True)
    analysisCompletedDate = models.DateTimeField(max_length=255, blank = True, null = True)
    def __str__(self):
        return self.name

class CovidUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    addressLine1 = models.CharField(max_length=512, blank = True, null = True)
    addressLine2 = models.CharField(max_length=512, blank = True, null = True)
    city = models.CharField(max_length=256, blank = True, null = True)
    state = models.CharField(max_length=2, blank = True, null = True)
    zipCode = models.CharField(max_length=12, blank = True, null = True)
    phoneNumber = models.CharField(max_length=12, blank = True, null = True)
    def __str__(self):
        return self.user.username

class CommentType(models.Model):
    userOrAlgorithm = models.BooleanField()
    algorithmUsed = models.CharField(max_length=256, blank = True, null = True)
    def __str__(self):
        return self.filePath

class Comment(models.Model):
    commentText = models.CharField(max_length=512)
    uploadFolder = models.ForeignKey(UploadFolder, on_delete=models.CASCADE)
    commentDate = models.DateTimeField()
    imageClass = models.IntegerField()
    xPosition = models.IntegerField()
    yPosition = models.IntegerField()
    zPosition = models.IntegerField()
    commentType = models.ForeignKey(CommentType, on_delete=models.CASCADE, blank = True, null = True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class Process(models.Model):
    name = models.CharField(max_length=512)
    description = models.CharField(max_length=512, blank = True, null = True)
    def __str__(self):
        return self.name

class ProcessStep(models.Model):
    name = models.CharField(max_length=512)
    # fileType = models.ForeignKey(FileType, blank = True, null = True )
    process  = models.ForeignKey ( Process , on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class LogFile(models.Model):
    antsCorticalThickness = models.CharField(max_length=512, blank = True, null = True)
    antsIntroduction = models.CharField(max_length=512, blank = True, null = True)
    jointLabelFusion = models.CharField(max_length=512, blank = True, null = True)
    warpImageMultiTransform = models.CharField(max_length=512, blank = True, null = True)
    uploadFolder = models.ForeignKey(UploadFolder, blank = True, null=True, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class JobStatusCode(models.Model):
    code = models.CharField(max_length=10)
    description = models.CharField(max_length=255, null=True)
    def __unicode__(self):
        return self.code

class SubmittedJob(models.Model):
    name = models.CharField(max_length=512)
    submittedBy = models.ForeignKey(User, on_delete=models.CASCADE)
    submittedOn = models.DateTimeField( null=True, blank = True)
    jobStatusCode = models.ForeignKey(JobStatusCode, on_delete=models.CASCADE)
    uploadeFolder = models.ForeignKey(UploadFolder, on_delete=models.CASCADE)
    completedTime = models.DateTimeField(null=True, blank=True)
    process = models.ForeignKey(Process, on_delete=models.CASCADE)
    def __unicode__(self):
        return self.name

class Species(models.Model):
    name = models.CharField(max_length=512)
    def __unicode__(self):
        return self.name

class Strain(models.Model):
    name = models.CharField(max_length=512)
    species = models.ForeignKey(Species, on_delete=models.CASCADE)
    def __unicode__(self):
        return self.name

class Sequence(models.Model):
    name = models.CharField(max_length=512)
    sequenceString = models.TextField()
    strain = models.ForeignKey(Strain, on_delete=models.CASCADE)
    def __unicode__(self):
        return self.name

class Gene(models.Model):
    name = models.CharField(max_length=512)
    sequence = models.TextField()
    strain = models.ManyToManyField(Sequence)
    def __unicode__(self):
        return self.name

class Mutation(models.Model):
    name = models.CharField(max_length=512)
    position = models.IntegerField()
    fromResidue = models.CharField(max_length=1)
    toResidue = models.CharField(max_length=1)
    def __unicode__(self):
        return self.name
class Taxon(models.Model):
    gb_taxon_id = models.CharField(max_length=20, unique=True)
    leaf = models.BooleanField()
    path = models.CharField(max_length=200)
    name = models.CharField(max_length=200, unique=True)
    level = models.CharField(max_length=50)
    def __str__(self): return self.name;
class Protein(models.Model):
    # organism = models.ForeignKey(Organism, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, unique=True)
    mesh_id = models.CharField(max_length=200, unique=True,  null=True)
    uniprot_id = models.CharField(max_length=200, unique=True, null=True )
    extrez_id = models.CharField(max_length=200, unique=True, null=True )

    def __str__(self): return self.name;
class Alignment(models.Model):
    name = models.CharField(max_length=100, unique=True)
    date_created = models.DateField(auto_now_add=True)
    def __str__(self): return self.name;
class ProteinSequence(models.Model):
    protein = models.ForeignKey(Protein, on_delete=models.CASCADE)
    taxon = models.ForeignKey(Taxon, on_delete=models.CASCADE)
    accession = models.CharField(max_length=50,unique=True)
    organism = models.CharField(max_length=200)
    collection_date = models.DateTimeField(null=True)
    country = models.CharField(max_length=100, null=True)
    host = models.CharField(max_length=100, null=True)
    isolation_source = models.CharField(max_length=100, null=True)
    coded_by = models.CharField(max_length=50, null=True)
    alignment = models.ForeignKey(Alignment, on_delete=models.CASCADE, null=True)
    sequence = models.TextField()
    offset = models.IntegerField()
    def __str__(self): return self.accession;
class Nomenclature(models.Model):
    name = models.CharField(max_length=100, unique=True)
    date_created = models.DateField(auto_now_add=True)
    alignment = models.ForeignKey(Alignment, on_delete=models.CASCADE)
    reference_proteinSequence = models.ForeignKey(ProteinSequence, blank=True, null=True, on_delete=models.SET_NULL)
    def __str__(self): return self.name;
class NomenClaturePositions(models.Model):
    index = models.IntegerField()
    nomenclature = models.ForeignKey(Nomenclature, on_delete=models.CASCADE)
    major = models.IntegerField() # major position relative to reference
    minor = models.IntegerField() # minor (or insert) relative to reference
    def __str__(self): return str(self.major)+'.'+str(self.minor).rjust(3,'0')
