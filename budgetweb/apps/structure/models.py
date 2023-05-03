from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class DomaineFonctionnel(models.Model):
    """
    Gestion des domaines fonctionnels. En cours de précisions
    """
    code = models.CharField(_('Code'), max_length=100, default="", unique=True)
    label = models.CharField(_('Label'), max_length=255, default="")
    label_court = models.CharField(_('Short label'), max_length=100, default="",
                                   null=True, blank=True,)
    is_active = models.BooleanField(_('Is active'), max_length=100, default=True)

    objects = models.Manager()
    active = ActiveManager()

    class Meta:
        verbose_name = _('functional domain')
        verbose_name_plural = _('functional domains')

    def __str__(self):
        return '{0.code} - {0.label_court}'.format(self)


class Structure(models.Model):
    """
    Gestion de la hiérarchie des Objets CF. En cours de précisions
    """
    code = models.CharField(_('Code'), max_length=100, unique=True)
    label = models.CharField(_('Label'), max_length=255)
    parent = models.ForeignKey(
        'Structure', blank=True, null=True, related_name='fils',
        verbose_name=u'Lien direct vers la structure parent',
        on_delete=models.CASCADE)
    groupe1 = models.CharField(_('BudgetWeb group 1'), max_length=255, blank=True, null=True)
    groupe2 = models.CharField(_('BudgetWeb group 2'), max_length=255, blank=True, null=True)
    is_active = models.BooleanField(_('Is active'), max_length=100, default=True)
    # Depth: 1 == root
    depth = models.PositiveIntegerField(_('Depth'))
    # Path: /id_root/id_ancestor1/id_ancestor2/...
    path = models.TextField(_('Path'), blank=True)

    objects = models.Manager()
    active = ActiveManager()

    class Meta:
        ordering = ['code']
        verbose_name = _('structure')
        verbose_name_plural = _('structures')

    def __str__(self):
        return '{0.code} - {0.label}'.format(self)

    def save(self, *args, **kwargs):
        parent = self.parent
        self.path = '{0.path}/{0.id}'.format(parent) if parent else ''
        self.depth = parent.depth + 1 if parent else 1
        super().save(*args, **kwargs)

    def get_ancestors_old(self):
        parent = self.parent
        return [parent] + parent.get_ancestors_old() if parent else []

    def get_ancestors(self):
        return Structure.objects.raw(
            """
            WITH RECURSIVE t(s_id) AS (
                VALUES (%s)
              UNION ALL
                SELECT s.parent_id from structure_structure as s, t where t.s_id = s.id
            )
            SELECT * FROM t, structure_structure s
            WHERE t.s_id = s.id AND t.s_id <> %s
            ORDER BY depth DESC
            """, (self.pk, self.pk)
        )

    def get_first_ancestor(self):
        if self.parent is None:
            return self
        else:
            return self.parent.get_first_ancestor()

    def get_children_old(self):
        children = []
        for sons in self.get_sons():
            children.append(sons)
            children.extend(sons.get_children_old())
        return children

    def get_children_from_path(self, *orders):
        return Structure.objects\
            .filter(Q(path__contains='/%s/' % self.pk) | Q(parent_id=self.pk))\
            .order_by(*orders)

    def get_children(self):
        return Structure.objects.raw(
            """
            WITH RECURSIVE t(s_id) AS (
                VALUES (%s)
              UNION ALL
                SELECT s.id from structure_structure as s, t where t.s_id = s.parent_id
            )
            SELECT * FROM t, structure_structure s
            WHERE t.s_id = s.id AND t.s_id <> %s
            ORDER BY code
            """, (self.pk, self.pk)
        )

    def get_sons(self):
        return self.fils.filter(is_active=True).order_by('code')

    @property
    def full_path(self):
        return '{0.path}/{0.pk}'.format(self)

    def get_full_path(self, order=True):
        ids = self.full_path.split('/')[1:]
        structures = list(Structure.objects.filter(pk__in=ids))
        if order:
            structures.sort(key=lambda s: ids.index(str(s.pk)))
        return structures


class PlanFinancement(models.Model):
    """
    Gestion des Plans de financement. En cours de précisions
    """
    structure = models.ForeignKey(
        'Structure', verbose_name=_('structure'), on_delete=models.CASCADE)
    code = models.CharField(_('Code'), max_length=100, default='NA')
    label = models.CharField(_('Label'), max_length=255)
    eotp = models.CharField(_('EOTP short label'), max_length=100)
    centrecoutderive = models.CharField(
        _('Related cost center'), max_length=100, null=True, blank=True)
    centreprofitderive = models.CharField(
        _('Related profit center'), max_length=100, null=True, blank=True)
    groupe1 = models.CharField(_('BudgetWeb group 1'), max_length=255,
                               null=True, blank=True)
    groupe2 = models.CharField(_('BudgetWeb group 2'), max_length=255,
                               null=True, blank=True)
    is_fleche = models.BooleanField(_('Is labeled'), default=False)
    is_pluriannuel = models.BooleanField(_('Is multi-year'), default=False)
    is_active = models.BooleanField(_('Is active'), max_length=100, default=True)
    date_debut = models.DateField(_('Begin date'), null=True, blank=True,
                                  help_text='Date de début')
    date_fin = models.DateField(_('End date'), null=True, blank=True,
                                help_text='Date de fin')

    objects = models.Manager()
    active = ActiveManager()

    class Meta:
        ordering = ['label']
        verbose_name = _('financial plan')
        verbose_name_plural = _('financial plans')

    def __str__(self):
        return '{0.structure.code} - {0.code}'.format(self)


class NatureComptableDepense(models.Model):

    enveloppe = models.CharField(_('Envelope'), max_length=100)
    label_nature_comptable = models.CharField(_('Label'), max_length=255)
    code_nature_comptable = models.CharField(_('Code'), max_length=100)
    code_compte_budgetaire = models.CharField(
        _('Budget account code'), max_length=100)
    label_compte_budgetaire = models.CharField(
        _('Budget account label'), max_length=255)
    is_fleche = models.BooleanField(
        _('Is labeled'), max_length=100, default=True)
    is_decalage_tresorerie = models.BooleanField(
        _('Is cash shift'), max_length=100)
    is_non_budgetaire = models.BooleanField(
        _('Is non budgetary'), max_length=100)
    is_pi_cfg = models.BooleanField(_('Is PFI/CFG'), max_length=100)
    is_active = models.BooleanField(
        _('Is active'), max_length=100, default=True)
    priority = models.PositiveIntegerField(
        _('Sorting order for the accounting natures'), default=1)
    ordre = models.PositiveIntegerField(
        _('Sorting sub-order for the accounting natures'), default=1)

    objects = models.Manager()
    active = ActiveManager()

    class Meta:
        verbose_name = _('expense accounting nature')
        verbose_name_plural = _('expenses accounting natures')

    def __str__(self):
        return '{0.code_nature_comptable} - {0.label_nature_comptable}'\
            .format(self)


class NatureComptableRecette(models.Model):

    enveloppe = models.CharField(_('Envelope'), max_length=100)
    code_fonds = models.CharField(_('Funds code'), max_length=100)
    label_fonds = models.CharField(_('Funds label'), max_length=255)
    code_nature_comptable = models.CharField(_('Code'), max_length=100)
    label_nature_comptable = models.CharField(_('Label'), max_length=255)
    code_compte_budgetaire = models.CharField(
        _('Budget account code'), max_length=100)
    label_compte_budgetaire = models.CharField(
        _('Budget account label'), max_length=255)
    is_fleche = models.BooleanField(
        _('Is labeled'), max_length=100, default=True)
    is_ar_and_re = models.BooleanField(_('Is AR et RE'), max_length=100)
    is_non_budgetaire = models.BooleanField(
        _('Is non budgetary'), max_length=100)
    is_active = models.BooleanField(_(
        'Is active'), max_length=100, default=True)
    priority = models.PositiveIntegerField(
        _('Sorting order for the accounting natures'), default=1)
    ordre = models.PositiveIntegerField(
        _('Sorting sub-order for the accounting natures'), default=1)

    objects = models.Manager()
    active = ActiveManager()

    class Meta:
        verbose_name = _('receipt accounting nature')
        verbose_name_plural = _('receipts accounting natures')

    def __str__(self):
        return '{0.code_nature_comptable} - {0.label_nature_comptable}'\
            .format(self)
